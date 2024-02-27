# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import Blueprint
from flask import current_app
from flask_limiter.errors import RateLimitExceeded
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from kadi.ext.talisman import talisman
from kadi.lib.api.core import json_error_response
from kadi.lib.api.utils import is_api_request
from kadi.lib.web import html_error_response


bp = Blueprint("main", __name__, template_folder="templates")


@bp.app_errorhandler(HTTPException)
def _app_errorhandler(e):
    # Before returning any error information, we redirect anonymous users using
    # Flask-Login's functionality to get consistent behavior with actual unauthorized
    # requests. We ignore CSRF-related errors (as this can interfere with the session
    # user loader) as well as rate limit and server errors.
    if (
        not isinstance(e, (CSRFError, RateLimitExceeded))
        and not e.code >= 500
        and not current_user.is_authenticated
    ):
        return current_app.login_manager.unauthorized()

    # If another pre-request handler aborts with an exception, the Flask-Talisman
    # handlers will never get called, so we call all of them manually here just in case,
    # even the ones not currently in use.
    talisman._force_https()
    talisman._make_nonce()

    if isinstance(e, RateLimitExceeded):
        description = f"Rate limit exceeded ({e.description}). Please try again later."
    else:
        description = e.description

    if is_api_request():
        response = json_error_response(e.code, description=description)
    else:
        response = html_error_response(e.code, description=description)

    talisman._set_response_headers(response)
    return response


from . import views  # pylint: disable=unused-import

from flask import Blueprint, render_template, request

from configuration.server_token import reg_token
from services.certs_manager import CertsManager

certs_bp = Blueprint("certs", __name__,
                    template_folder='../templates',
                    static_folder='../static')

@certs_bp.route("/certs")
@certs_bp.route("/certs/")
def certs_default():
    token = request.args.get("token")
    if token == reg_token:
        return render_template("certs.html", certs=CertsManager().certs)
    return render_template("certs.html", certs=[])
    

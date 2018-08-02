from flask import Flask, request, render_template
from nimbusland import Nimbusland

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def nimbusland():
    error = False
    ip_info = ''
    error_message = ''

    if request.method == 'POST':
        try:
            target_ip = request.form['target_ip']
            nl = Nimbusland()
            ip_info = nl.get_aws_ip_info(target_ip)
            ip_info = ip_info if ip_info else nl.get_azure_ip_info(target_ip)

        except Exception as e:
            error = True
            error_message = str(e)

    return render_template('index.html', ip_info=ip_info, error=error, error_message=error_message)


if __name__ == '__main__':
    app.run()

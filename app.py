"""
APP WEB (Flask) - Vista web del proyecto, REUTILIZA la clase Modelo del MVC.
Ejecutar:  python app.py   ->   abrir http://localhost:5000
Requiere:  pip install flask
"""

from flask import Flask, request, redirect, url_for, render_template_string
from modelo import Modelo

app = Flask(__name__)

PLANTILLA = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Datos Colombia</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f3f4f6;color:#111827}
    header{background:#1f2937;color:#fff;padding:16px 24px}
    main{max-width:900px;margin:24px auto;padding:0 16px}
    .card{background:#fff;border-radius:8px;padding:20px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
    h1{margin:0;font-size:20px}
    h2{font-size:16px;border-bottom:2px solid #2563eb;padding-bottom:6px}
    table{width:100%;border-collapse:collapse;margin-top:12px}
    th,td{text-align:left;padding:8px;border-bottom:1px solid #e5e7eb}
    th{background:#f9fafb}
    form.inline{display:inline}
    input,button{padding:8px;border:1px solid #d1d5db;border-radius:6px;font-size:14px}
    button{background:#2563eb;color:#fff;border:none;cursor:pointer}
    button.danger{background:#dc2626}
    .row{display:flex;gap:8px;flex-wrap:wrap;align-items:end}
    .field{display:flex;flex-direction:column;gap:4px}
    label{font-size:12px;font-weight:bold}
  </style>
</head>
<body>
  <header><h1>Sistema Datos Colombia (Web)</h1></header>
  <main>
    <div class="card">
      <form method="post" action="{{ url_for('recargar') }}">
        <button type="submit">Recargar datos desde la API</button>
      </form>
    </div>

    <div class="card">
      <h2>Crear registro</h2>
      <form method="post" action="{{ url_for('crear') }}">
        <div class="row">
          <div class="field"><label>Ciudad</label><input name="ciudad" required></div>
          <div class="field"><label>Departamento</label><input name="departamento" required></div>
          <div class="field"><label>Edad</label><input name="edad" type="number" required></div>
          <button type="submit">Agregar</button>
        </div>
      </form>
    </div>

    <div class="card">
      <h2>Registros actuales</h2>
      <table>
        <tr><th>ID</th><th>Ciudad</th><th>Departamento</th><th>Edad</th><th>Acciones</th></tr>
        {% for r in registros %}
        <tr>
          <td>{{ r[0] }}</td>
          <td>{{ r[1] }}</td>
          <td>{{ r[2] }}</td>
          <td>{{ r[3] }}</td>
          <td>
            <form class="inline" method="post" action="{{ url_for('actualizar') }}">
              <input type="hidden" name="id" value="{{ r[0] }}">
              <input name="ciudad" placeholder="Nueva ciudad" required>
              <button type="submit">Actualizar</button>
            </form>
            <form class="inline" method="post" action="{{ url_for('eliminar') }}">
              <input type="hidden" name="id" value="{{ r[0] }}">
              <button type="submit" class="danger">Eliminar</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="5">La tabla esta vacia.</td></tr>
        {% endfor %}
      </table>
    </div>

    <div class="card">
      <h2>Analisis por departamento</h2>
      <table>
        <tr><th>Departamento</th><th>Total registros</th><th>Edad promedio</th></tr>
        {% for a in analisis %}
        <tr><td>{{ a[0] }}</td><td>{{ a[1] }}</td><td>{{ "%.1f"|format(a[2]|float) }}</td></tr>
        {% endfor %}
      </table>
    </div>
  </main>
</body>
</html>
"""


@app.route("/")
def index():
    m = Modelo()
    registros = m.leer()
    analisis = m.analisis()
    m.cerrar()
    return render_template_string(PLANTILLA, registros=registros, analisis=analisis)


@app.route("/recargar", methods=["POST"])
def recargar():
    m = Modelo()
    m.cargar_desde_api()
    m.cerrar()
    return redirect(url_for("index"))


@app.route("/crear", methods=["POST"])
def crear():
    m = Modelo()
    m.crear(request.form["ciudad"], request.form["departamento"], int(request.form["edad"]))
    m.cerrar()
    return redirect(url_for("index"))


@app.route("/actualizar", methods=["POST"])
def actualizar():
    m = Modelo()
    m.actualizar(int(request.form["id"]), request.form["ciudad"])
    m.cerrar()
    return redirect(url_for("index"))


@app.route("/eliminar", methods=["POST"])
def eliminar():
    m = Modelo()
    m.eliminar(int(request.form["id"]))
    m.cerrar()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
<!DOCTYPE html>
<html>
  <head>
      <title>Control de cámara</title>
      <link rel="stylesheet" href="assets/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
      <meta name="viewport" content="width=device-width, user-scalable=no">
  </head>

  <?php
    function execInBackground($cmd) {
      shell_exec($cmd . " > /dev/null & echo $!");
    }

    function estadoCamara() {
      $res = shell_exec("ps aux | grep -i 'vigilancia.py' | grep -v 'grep' | wc -l");
      if ($res == 0) {
        echo "Apagado";
      } else {
        echo "Encendido";
      };
    }
  ?>

  <?php
    if(array_key_exists('button1', $_POST)) {
      button1();
    }
    if(array_key_exists('button2', $_POST)) {
      button2();
    }

    function button1() {
      execInBackground('python3 -m pipenv run python3 ./vigilancia.py');
    }

    function button2() {
      execInBackground("killall python3");
    }
  ?>

  <body style="text-align:center;">
    <div class="container p-5">
      <div class="row">
        <div class="col-sm p-2 mb-5">
          <img src="assets/unaj-logo.png" class="img-fluid" alt="Unaj-logo">
        </div>
      </div>
      <div class="row">
        <div class="col-sm p-2 mb-5">
          <h1>Sistema de detección de movimiento</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-sm p-2">
          <h4>Estado del sistema: <?php estadoCamara(); ?> </h4>
        </div>
      </div>
      <div class="row">
        <div class="col-sm">
          <form class="form-inline" method="post" style="justify-content:center;">
            <div class="form-group mb-2">
              <input type="submit" name="button1" class="btn btn-primary" value="Encender cámara" />
            </div>
            <div class="form-group mx-sm-3 mb-2">
              <input type="submit" name="button2" class="btn btn-dark" value="Apagar cámara" />
            </div>
          </form>
        </div>
      </div>
    </div>
  </body>
  <script>
    window.stop();
  </script>
</html>

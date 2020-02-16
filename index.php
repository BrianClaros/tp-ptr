<!DOCTYPE html>
<html>
  <head>
      <title>Control de cámara</title>
  </head>

  <body style="text-align:center;">
    <h1 style="color:green;">
        TP PTR
    </h1>

    <?php
      function execInBackground($cmd) {
        shell_exec($cmd . " > /dev/null & echo $!");
      }
    ?>

    <?php
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

    <h3>Estado: <?php estadoCamara(); ?> </h3>

    <form method="post">
      <input type="submit" name="button1"
              class="button" value="Encender cámara" />

      <input type="submit" name="button2"
              class="button" value="Apagar cámara" />
    </form>
  </body>
</html>
<!DOCTYPE html>
<html>

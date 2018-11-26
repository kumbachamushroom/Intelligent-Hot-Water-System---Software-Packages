<!DOCTYPE html>
<?php
   $Temp = '';
   $Name = '';
   $Error = '';
   $Switch = '';


   function clean_text($string)
   {
   $string = trim($string);
   $string = stripslashes($string);
   $string = htmlspecialchars($string);
   return $string;
   }
   if(isset($_POST["submit"]))
   {
    $Temp = clean_text($_POST["temp"]);
    $Switch = $_POST["onoffswitch"];
    if ($_POST["onoffswitch"]== '1'){
   $on_off = 'on';
   }
   else {
   $on_off = 'off';
   }
       if($error == ''){
     $file_open = fopen("temp.txt", "w");
           $form_data = array('Temp'=> $Temp, 'OnOff' => $on_off);
            fputcsv($file_open, $form_data);
            }
            }
   ?>
<html lang="en">
   <head>
      <title>EVEREADY</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
      <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
      <script type="text/javascript" src="http://static.pureexample.com/js/flot/jquery.flot.min.js"></script>
      <script type="text/javascript" src="http://static.pureexample.com/js/flot/jquery.flot.time.js"></script>
      <script type="text/javascript" src="http://static.pureexample.com/js/flot/jquery.flot.axislabels.js"></script>
      <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
   </head>
   <style>
      .style1 {
      margin-left: 24px;
      background-color: #E6E6E6;
      }
      .slidecontainer {
      width: 50%;
      }
      .slider {
      -webkit-appearance: none;
      width: 50%;
      border-radius: 5px;
      height: 15px;
      background: #6E6E6E;
      outline: none;
      opacity: 0.7;
      -webkit-transition: .2s;
      transition: opacity .2s;
      }
      .slider:hover {
      opacity: 1;
      }
      .slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 25px;
      height: 25px;
      border-radius: 50%;
      background: #4CAF50;
      cursor: pointer;
      }
      .slider::-moz-range-thumb {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      background: #4CAF50;
      cursor: pointer;
      }
      .onoffswitch {
      position: relative; width: 84px;
      -webkit-user-select:none; -moz-user-select:none; -ms-user-select: none;
      }
      .onoffswitch-checkbox {
      display: none;
      }
      .onoffswitch-label {
      display: block; overflow: hidden; cursor: pointer;
      border: 2px solid #999999; border-radius: 20px;
      }
      .onoffswitch-inner {
      display: block; width: 200%; margin-left: -100%;
      transition: margin 0.3s ease-in 0s;
      }
      .onoffswitch-inner:before, .onoffswitch-inner:after {
      display: block; float: left; width: 50%; height: 36px; padding: 0; line-height: 36px;
      font-size: 12px; color: white; font-family: Trebuchet, Arial, sans-serif; font-weight: bold;
      box-sizing: border-box;
      }
      .onoffswitch-inner:before {
      content: "ON";
      padding-left: 14px;
      background-color: #34A7C1; color: #FFFFFF;
      }
      .onoffswitch-inner:after {
      content: "OFF";
      padding-right: 14px;
      background-color: #EEEEEE; color: #999999;
      text-align: right;
      }
      .onoffswitch-switch {
      display: block; width: 15px; margin: 12.5px;
      background: #FFFFFF;
      position: absolute; top: 0; bottom: 0;
      right: 44px;
      border: 2px solid #999999; border-radius: 20px;
      transition: all 0.3s ease-in 0s;
      }
      .onoffswitch-checkbox:checked + .onoffswitch-label .onoffswitch-inner {
      margin-left: 0;
      }
      .onoffswitch-checkbox:checked + .onoffswitch-label .onoffswitch-switch {
      right: 0px;
      }
   </style>
   <style type="text/css">
      #flotcontainer {
      width: 90vw;
      height: 30vh;
      text-align: center;
      margin: 0 auto;
      }
   </style>
   <script>
      var data = [];
      var dataset;
      var totalPoints = 300;
      var updateInterval = 1000;
      var now = new Date().getTime();


      function GetData() {
          data.shift();

          while (data.length < totalPoints) {
              var y = parseFloat(document.getElementById("Temperature").innerHTML);
              var temp = [now += updateInterval, y];

              data.push(temp);
          }
      }

      var options = {
          series: {
              lines: {
                  show: true,
                  lineWidth: 1.2,
                  fill: true
              }
          },
          xaxis: {
    mode: "time",
    tickSize: [20, "second"],
    tickFormatter: function (v, axis) {
        var date = new Date(v);

        if (date.getSeconds() % 20 == 0) {
            var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
            var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
            var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

            return hours + ":" + minutes + ":" + seconds;
        } else {
            return "";
        }
    },
    axisLabel: "Time",
    axisLabelUseCanvas: true,
    axisLabelFontSizePixels: 12,
    axisLabelFontFamily: 'Verdana, Arial',
    axisLabelPadding: 10
},
          yaxis: {
              min: 0,
              max: 100,
              tickSize: 10,
              tickFormatter: function (v, axis) {
                  if (v % 20 == 0) {
                      return v + "°C";
                  } else {
                      return "";
                  }
              },
              axisLabel: "Temperature (°C)",
              axisLabelUseCanvas: true,
              axisLabelFontSizePixels: 12,
              axisLabelFontFamily: 'Verdana, Arial',
              axisLabelPadding: 6
          },
          legend: {
              labelBoxBorderColor: "#fff"
          }
      };

      $(document).ready(function () {
          GetData();

          dataset = [
              { label: "Temperature", data: data, color: "#F8483F" }
          ];

          $.plot($("#flotcontainer"), dataset, options);

          function update() {
              GetData();

              $.plot($("#flotcontainer"), dataset, options)
              setTimeout(update, updateInterval);
          }

          update();
      });



   </script>
   <body class="style1">
      <div class="col-sm-12">
         <h2>Intelligent Hot Water System</h2>
         <h4>Current Temperature: <span id = "Temperature" ></span><span>&#176;</span>C</h4>
         <h4>Current: <span id = "Current" ></span>A</h4>
         <iframe name="votar" style="display:none;"></iframe>
         <form action="" method="post" target="votar">
            <h2>Heating</h2>
            <div class="onoffswitch">
               <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="myonoffswitch" onclick="getValue()" <?php echo $Switch== '1' ? ' checked' : ''; ?> >
               <label class="onoffswitch-label" for="myonoffswitch">
               <span class="onoffswitch-inner"></span>
               <span class="onoffswitch-switch"></span>
               </label>
            </div>
            <div></div>
            <div class="slidecontainer">
               <p>Select Temperature (Range 0 to 100):</p>
               <input type="range" name = "temp" min="0" max="100" value="<?php echo $Temp; ?>" class="slider" id="myRange">
               <p>Value: <span id="demo"></span><span>&#176;</span>C</p>
            </div>
            <script>
               var slider = document.getElementById("myRange");
               var output = document.getElementById("demo");
               output.innerHTML = slider.value;

               slider.oninput = function() {
                 output.innerHTML = this.value;
               }
            </script>
            <input type="submit" name="submit" class="btn btn-info" value="Submit" onclick="getValue()" />
         </form>
         <div align="center">
            <h4>Temperature over time</h4>
            <div id="flotcontainer"></div>
         </div>
         <h3>Diagnostic info</h3>
         <div>
           Date select:
           <input type="date" data-date-format="DD MMMM YYYY" name="bday" id="dateToUse">
           <button type="button" name="avg" id="avg" class="btn btn-info">Show Diagnostic info</button>
           <div id="Avg_C"></div>
           <div id="Avg_T"></div>
           <div id="max_C"></div>
           <div id="max_T"></div>
           <div id="min_T"></div>
           <div id="min_C"></div>
         </div>
         <script type="text/javascript">
            function getValue() {
               var isChecked = document.getElementById("myonoffswitch").checked;


               if(isChecked){
                 console.log("Input is checked");
                 document.getElementById("myonoffswitch").value = '1';
                 isChecked.innerHTML = '1';
               } else {
                 console.log("Input is NOT checked");
                 document.getElementById("myonoffswitch").value = "0";
                 isChecked.innerHTML = '0';
               }
            }
         </script>
         </tbody>
         <div class="container">
            <div class="table-responsive">
               <h1 align="center">Diagnostic data</h1>
               <br />
               <div align="center">
                  <button type="button" name="load_data" id="load_data" class="btn btn-info">Load Data</button>
               </div>
               <br />
               <div id="Diagnostic">
               </div>
            </div>
         </div>
      </div>
      <script>
      $('#avg').click(function(){
        var dateToUse =document.getElementById("dateToUse").value
        dateToUse = convertDate(dateToUse);
        console.log(dateToUse);
        d3.csv('test.csv',function(data){
          var data1 = data.filter(function(d) {return d.Date == dateToUse;})
          if (data1.length > 0) {
            var avgC = d3.mean(data1, function(d) { return d.Current; });
            var avgT = d3.mean(data1, function(d) { return d.Temperature; });
            var maxT = d3.max(data1, function(d) { return d.Temperature; });
            var maxC = d3.max(data1, function(d) { return d.Current; });
            var minC = d3.min(data1, function(d) { return d.Temperature; });
            var minT = d3.min(data1, function(d) { return d.Current; });


            avgC = avgC.toFixed(2)
            avgT = avgT.toFixed(2)
            var avg_C = 'Average Current: '+avgC+' A'
            var avg_T = 'Average Temperature: '+avgT+' <span>&#176;</span>C'
            var max_C = 'Max Current: '+maxC+' A'
            var max_T = 'Max Temperature: '+maxT+' <span>&#176;</span>C'
            var min_C = 'Min Current: '+minC+' A'
            var min_T = 'Min Temperature: '+minT+' <span>&#176;</span>C'
            $('#Avg_C').html(avg_C);
            $('#Avg_T').html(avg_T);
            $('#max_C').html(max_C);
            $('#max_T').html(max_T);
            $('#min_C').html(min_C);
            $('#min_T').html(min_T);
            console.log(avgC);
            console.log(data1);
          }
          else {
            var NoData = 'No data for that date'
            $('#Avg_C').html(NoData);
          }

        })
      });
      function convertDate(inputFormat) {
        function pad(s) { return (s < 10) ? '0' + s : s; }
        var d = new Date(inputFormat);
        return [ pad(d.getDate()), pad(d.getMonth()+1), d.getFullYear()].join('.');
      }
      </script>
      <script type="text/javascript">
         $(document).ready( function(){
           $('#Temperature').load('load.php');
           $('#Current').load('data.php');
           refresh();
         });

         function refresh()
         {
           setTimeout( function() {
             $('#Temperature').load('load.php');
             $('#Current').load('data.php');
             refresh();
           }, 1000);
         }

      </script>
   </body>
   <script>
      $(document).ready(function(){
       $('#load_data').click(function(){
        $.ajax({
         url:"databackup.csv",
         dataType:"text",
         success:function(data)
         {
          var employee_data = data.split(/\r?\n|\r/);
          var table_data = '<table class="table table-bordered table-striped">';
          for(var count = 0; count<employee_data.length; count++)
          {
           var cell_data = employee_data[count].split(",");
           table_data += '<tr>';
           for(var cell_count=0; cell_count<cell_data.length; cell_count++)
           {
            if(count === 0)
            {
             table_data += '<th>'+cell_data[cell_count]+'</th>';
            }
            else
            {
             table_data += '<td>'+cell_data[cell_count]+'</td>';
            }
           }
           table_data += '</tr>';
          }
          table_data += '</table>';
          $('#Diagnostic').html(table_data);
         }
        });
       });

      });
   </script>
</html>

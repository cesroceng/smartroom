<?php
include "dbConfig.php";
	session_start();
	if ($_SESSION['loggedin']==FALSE)
	{
		header('Location: index.php');
	}
	
	if( isset($_GET['selectedDate']) ) {
		$selectedDate = $_GET["selectedDate"];
	}
	else {
		$selectedDate = date('Y-m-d');
	}
?>

<!DOCTYPE html>
<html>
	<?php 
					header("refresh: 600"); 
				  $result = $link->query("SELECT date,temp1,temp2,light1,light2,motion FROM meas ORDER BY id DESC LIMIT 1");
				  $row = $result->fetch_assoc();
	?>
	<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	<head>
		<meta charset="utf8">
		<title>SmartCities Project</title>
		<link href="style1.css" rel="stylesheet" type="text/css">
		<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
		<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
		<script>
			$(document).ready(function(){
      	$('#dateGraph').change(function(){
      		//Selected value
      		var inputValue = $(this).val();
        	window.open("home.php?selectedDate="+inputValue, "_self");
      	});
			});
	</script>
	</head>
	<body class="loggedin">
		<nav class="navtop">
			<div>
				<h1>SmartCities Project</h1>
				<a href="logout.php"><i class="fas fa-sign-out-alt"></i>Logout</a>
			</div>
		</nav>
		<div class="content">
		<h2>Last Temperature Measured (<?php echo $row['date'];?>):</h2>
			<p>
				<?php 
					echo "Inside: "; echo $row['temp1']; echo "°C";
					echo "<br>";
					echo "Outside: "; echo $row['temp2']; echo "°C";
				?>
			</p>
			<h2>Last State of Light (<?php echo $row['date'];?>):</h2>
			<p>
				<?php 
					if ($row['light1']>7000) {
						echo "Inside: Dark";
					}
					else {
						echo "Inside: Bright";
					}
					echo "<br>";
					if ($row['light2']>10000) {
						echo "Outside: Dark";
					}
					else {
						echo "Outside: Bright";
					}
				?>
			</p>
			<h2>Last State of Movement (<?php echo $row['date'];?>):</h2>
			<p>
				<?php 
					if ($row['motion']==1) {
						echo "People in the room";
					}
					else {
						echo "Room is empty";
					}
				?>
			</p>
			<?php 
				  $result = $link->query("SELECT date FROM meas");

					$a = [];
				  while ($row = $result->fetch_assoc()) {
				  	$rowArray = explode('|', $row['date']);
    				$a[] = $rowArray[0];
					}
					
					$dateArray[] = $a[0];
					$found = false;
					
					for ($i = 0; $i < count($a); $i++) {
						for ($j = 0; $j < count($dateArray); $j++) {
    					if($a[$i]==$dateArray[$j]){
    						$found = true;
    					}
						}
						if ($found==true){
							$found = false;
						}
						else
						{
							$dateArray[] = $a[$i];
						}
					}
					
					$dateArray = array_reverse($dateArray);
			?>

<?php 
	$query = $link->query("SELECT * FROM output ORDER BY id DESC LIMIT 1");
		$radiator = "gray";
		$blinds = "gray";
		$window = "gray";
		$lights = "gray";
		while($row = $query->fetch_assoc()){
		$pos = stristr($row['radiator'],"OPEN");
		if ($pos) {
			$radiator = "green";
		}
		$pos = stristr($row['blinds'],"OPEN");
		if ($pos) {
			$blinds = "green";
		}
		$pos = stristr($row['window'],"OPEN");
		if ($pos) {
			$window = "green";
		}
		$pos = stristr($row['lights'],"TURNON");
		if ($pos) {
			$lights = "green";
		}
					}
?>
			<h2>FS Planner Decision (Green: On/Open | Gray Off/Closed):</h2>
			<p>



				<span style="vertical-align:100%;">Radiator: </span>
				<svg width="50" height="50">
					<circle cx="25" cy="25" r="15" stroke="black" stroke-width="2" fill=<?php echo $radiator; ?> />
					Sorry, your browser does not support inline SVG.
				</svg>
				<span style="vertical-align:100%;">Lights: </span>
				<svg width="50" height="50">
					<circle cx="25" cy="25" r="15" stroke="black" stroke-width="2" fill=<?php echo $lights; ?> />
				</svg>
				<span style="vertical-align:100%;"> Blinds: </span>
				<svg width="50" height="50">
					<circle cx="25" cy="25" r="15" stroke="black" stroke-width="2" fill=<?php echo $blinds; ?> />
				</svg>
				<span style="vertical-align:100%;"> Windows: </span>
				<svg widht="50" height="50">
					<circle cx="25" cy="25" r="15" stroke="black" stroke-width="2" fill=<?php echo $window; ?> />
				</svg>
			</p>
			<h2>Select a date from database:
					<select id="dateGraph" name="DateGraph" >
						<?php
							echo '<option>Select another date</option>';
							for ($i = 0; $i < count($dateArray); $i++) {
								echo '<option>' . $dateArray[$i] . '</option>';
   					}
						?>
					</select>
				</h2>
			<h2>History of Temperature: <?php echo $selectedDate; ?>:</h2>
				<?php
					$selectedDate = str_replace(' ', '', $selectedDate);
					$result = $link->query("SELECT * FROM meas");

					$time   = [];
					$temp1  = [];
					$temp2  = [];
					$light1 = [];
					$light2 = [];
					$motion = [];
				  while ($row = $result->fetch_assoc()) {
				  	$pos = strpos($row['date'], $selectedDate);
				  	if ($pos === 0) {
				  		$time[]   = str_replace(' ', '', explode('|', $row['date'])[1]);
				  		$temp1[]  = $row['temp1'];
    					$temp2[]  = $row['temp2'];
    					$light1[] = $row['light1'];
							$light2[] = $row['light2'];
							$motion[] = $row['motion'];
				  	}
    				
					}

					$dataPoints  = [];
					$dataPoints1 = [];
					$dataPointsLight1 = [];
					$dataPointsLight2 = [];
					$dataPointsMotion = [];	
					for ($i = 0; $i < count($temp1); $i++) {
						$convertedLight1 = 0;
						$convertedLight2 = 0;
						
						if ($light1[$i] > 7000) {
							$convertedLight1 = 0;
						}
						else {
							$convertedLight1 = 1;
						}
						
						if ($light2[$i] > 7000) {
							$convertedLight2 = 0;
						}
						else {
							$convertedLight2 = 1;
						}
							
						$dataPointsTemp1[] = array("y" => $temp1[$i]+"°C", "label" => $time[$i]);
						$dataPointsTemp2[] = array("y" => $temp2[$i]+"°C", "label" => $time[$i]);
						$dataPointsLight1[] = array("y" => $convertedLight1, "label" => $time[$i]);
						$dataPointsLight2[] = array("y" => $convertedLight2, "label" => $time[$i]);
						$dataPointsMotion[] = array("y" => $motion[$i], "label" => $time[$i]);
					}

				?>
				<script>
						window.onload = function () {
 						var chart1 = new CanvasJS.Chart("temp_graph", {
								title: {
									text: "Temperature changing during the day"
								},
								axisY: {
									title: "Temperature (°C)"
								},
							data: [{
								type: "line",
								yValueFormatString: "#,##0 °C",
								showInLegend: true,
								legendText: "Temperature Inside",
								dataPoints: <?php echo json_encode($dataPointsTemp1, JSON_NUMERIC_CHECK); ?>
							},
							{
								type: "line",
								yValueFormatString: "#,##0 °C",
								showInLegend: true,
								legendText: "Temperature Outside",
								dataPoints: <?php echo json_encode($dataPointsTemp2, JSON_NUMERIC_CHECK); ?>
							},
							]
						});
						var chart2 = new CanvasJS.Chart("light_graph", {
								title: {
									text: "Light changing during the day"
								},
								axisY: {
									title: "Light (0-Dark; 1-Bright)"
								},
							data: [{
								type: "line",
								showInLegend: true,
								legendText: "Light Inside",
								dataPoints: <?php echo json_encode($dataPointsLight1, JSON_NUMERIC_CHECK); ?>
							},
							{
								type: "line",
								showInLegend: true,
								legendText: "Light Outside",
								dataPoints: <?php echo json_encode($dataPointsLight2, JSON_NUMERIC_CHECK); ?>
							},
							]
						});
						var chart3 = new CanvasJS.Chart("motion_graph", {
								animationEnabled: true,
								theme: "light2",
								title: {
									text: "Movement inside the room"
								},
								axisY: {
									title: "0-Room Empty; 1-People Inside)"
								},
							data: [{
								type: "column",
								dataPoints: <?php echo json_encode($dataPointsMotion, JSON_NUMERIC_CHECK); ?>
							}
							]
						});
						chart1.render();
						chart2.render();
						chart3.render();
 
					}
				</script>
				<div id="temp_graph" style="height: 250px; width: 950px;"></div>
				<h2>History of Light for <?php echo $selectedDate; ?>:</h2>
				<div id="light_graph" style="width: 950px; height: 250px"></div>
			<h2>History of Movement for <?php echo $selectedDate; ?>:</h2>
				<div id="motion_graph" style="width: 950px; height: 250px"></div>
			<h2>FF Planner Output:</h2>
			<p><?php echo nl2br(file_get_contents("/home/smartcities/Documents/Output.txt",true)); ?></p>
		</div>
	</body>
</html>

<!doctype html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang=""> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8" lang=""> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9" lang=""> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"  lang="en"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="apple-touch-icon" href="apple-touch-icon.png">
		<link rel="stylesheet" href="assets/css/style.css">
        <script src="assets/js/vendor/modernizr-2.8.3-respond-1.4.2.min.js"></script>
		<link href="https://fonts.googleapis.com/css?family=Ubuntu:300,300i,400,400i,500,500i,700,700i" rel="stylesheet">
    </head>
    <body>
        <!--[if lt IE 8]>
            <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->
			<?php include 'header.php';?>
			<div id="main-content" class="padding">
				<section class="panel">
                    <header class="panel-heading clearfix">
                        <h3>Site Map</h3>
                    </header>
                    <div class="panel-body">
						<div id="osMap" class="full-map margin-top"></div>
                    </div>
                </section>
				<div class="row">
					<div class="col-md-3">
						<div class="mini-stat padding-large margin-top clearfix">
							<span class="mini-stat-icon"><i class="la la-users"></i></span>
							<div class="mini-stat-info">
								<span>129</span>
								Total Users
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="mini-stat padding-large margin-top clearfix">
							<span class="mini-stat-icon"><i class="la la-building"></i></span>
							<div class="mini-stat-info">
								<span>10</span>
								Total Organizations
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="mini-stat padding-large margin-top clearfix">
							<span class="mini-stat-icon"><i class="la la-tasks"></i></span>
							<div class="mini-stat-info">
								<span>38</span>
								Total Projects
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="mini-stat padding-large margin-top clearfix">
							<span class="mini-stat-icon"><i class="la la-sitemap"></i></span>
							<div class="mini-stat-info">
								<span>407</span>
								Total Sites
							</div>
						</div>
					</div>
				</div>
			</div>
		<?php include 'footer.php';?>
		<script src="assets/js/vendor/leaflet.js"></script>
		<script>
			var map = L.map('osMap', {
				center: [51.505, -0.09],
				zoom: 13
			});
			

		</script>

        <script src="assets/js/plugins.js"></script>
        <script src="assets/js/main.js"></script>
		
    </body>
</html>

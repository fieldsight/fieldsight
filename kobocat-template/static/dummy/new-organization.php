<!doctype html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang=""> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8" lang=""> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9" lang=""> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
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
                        <h3><i class="la la-building"></i>New Organization</h3>
                    </header>
					<div class="panel-body">
						<!-- Add New Organization-->
						<div id="newOrganization" class="margin-top">
							<form>
								<div class="form-row">
									<div class="form-group col-md-6">
									  <label for="input1" class="col-form-label">Organization Name :</label>
									  <input type="text" class="form-control" id="input1">
									</div>
									<div class="form-group col-md-6">
									  <label for="input2" class="col-form-label">Type of Organization :</label>
									  <select id="input2" class="form-control">
										<option selected>Choose...</option>
										<option>Government</option>
										<option>Local NGO</option>
										<option>INGO</option>
										<option>Local Business</option>
										<option>Multi National</option>
									  </select>
									</div>
									<div class="form-group col-md-6">
									  <label for="input3" class="col-form-label">Contact Number :</label>
									  <input type="text" class="form-control" id="input3">
									</div>
									<div class="form-group col-md-6">
									  <label for="input4" class="col-form-label">Fax :</label>
									  <input type="text" class="form-control" id="input4">
									</div>
									<div class="form-group col-md-6">
									  <label for="input5" class="col-form-label">Email :</label>
									  <input type="text" class="form-control" id="input5">
									</div>
									<div class="form-group col-md-6">
									  <label for="input6" class="col-form-label">Website :</label>
									  <input type="text" class="form-control" id="input6">
									</div>
									<div class="form-group col-md-4">
									  <label for="input7" class="col-form-label">Country :</label>
									  <select id="input7" class="form-control">
										<option selected>Choose...</option>
										<option>Nepal</option>
										<option>Australia</option>
										<option>United States</option>
										<option>Japan</option>
									  </select>
									</div>
									<div class="form-group col-md-8">
									  <label for="input8" class="col-form-label">Address :</label>
										<input type="text" class="form-control" id="input8">
									</div>
									<div class="form-group col-md-6">
									  <label for="input9" class="col-form-label">Public Description :</label>
										<textarea class="form-control" id="input9" rows="5"></textarea>
									</div>
									<div class="form-group col-md-6">
									  <label for="input10" class="col-form-label">Additional Description :</label>
										<textarea class="form-control" id="input10" rows="5"></textarea>
									</div>
									<div class="form-group col-md-6">
									  <label for="input11" class="col-form-label">Latitude :</label>
									  <input type="text" class="form-control" id="input11">
									</div>
									<div class="form-group col-md-6">
									  <label for="input12" class="col-form-label">Longitude :</label>
									  <input type="text" class="form-control" id="input12">
									</div>
									<!--<div class="form-group col-md-12">
										<label class="custom-file">
										  <input type="file" id="file2" class="custom-file-input">
										  <span class="custom-file-control"></span>
										</label>
									</div>-->
									<div class="form-group col-md-12">
									  <label class="custom-control custom-checkbox">
										<input type="checkbox" class="custom-control-input" checked>
										<span class="custom-control-indicator"></span>
										<span class="custom-control-description">Is Active</span>
									  </label>
									</div>
									<div class="form-group col-md-12">
										<div id="osMap" class="full-map margin-top"></div>
									</div>
								</div>
								<button type="submit" class="btn btn-primary"><i class="la la-plus"></i> Add Organization</button>
							</form>
						</div>
					</div>
                </section>
				
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
		

        <!-- Google Analytics: change UA-XXXXX-X to be your site's ID. -->
        <script>
            (function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
            function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
            e=o.createElement(i);r=o.getElementsByTagName(i)[0];
            e.src='//www.google-analytics.com/analytics.js';
            r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
            ga('create','UA-XXXXX-X','auto');ga('send','pageview');
        </script>
    </body>
</html>

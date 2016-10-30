require('es6-promise').polyfill();

// Defining base pathes
var basePaths = {
  bower: './bower_components/',
  temp: './tmp/',
  target: './webapp/static/',
  assets: './assets/'
};

// requirements
var gulp = require('gulp');
var concat = require('gulp-concat');
var cssnano = require('gulp-cssnano');
var googleWebFonts = require('gulp-google-webfonts');
var ignore = require('gulp-ignore');
var plumber = require('gulp-plumber');
var rename = require('gulp-rename');
var replace = require('gulp-replace');
var rimraf = require('gulp-rimraf');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');
var merge2 = require('merge2');

// gulp clean
gulp.task('clean', function() {
  gulp.src(basePaths.temp, { read: false })
    .pipe(rimraf())
});

// gulp watch
gulp.task('watch', function () {
  // JS
  gulp.watch(basePaths.assets + 'js/*.js', function(event){ gulp.run('copy-assets-webapp-js', 'concat-js' )});
  // CSS
  gulp.watch(basePaths.assets + 'sass/*.scss', function(event){ gulp.run('copy-assets-webapp-css', 'sass', 'concat-css' )});
});

// gulp sass
gulp.task('sass', function () {
  gulp.src(basePaths.temp + 'sass/*.scss')
    .pipe(plumber())
    .pipe(sass({noCache: true}))
    .pipe(gulp.dest(basePaths.temp + 'css/'));
});

// gulp concat-css
gulp.task('concat-css', function() {
  return gulp.src(basePaths.temp + 'css/base.css')
    .pipe(plumber())
    .pipe(rename({suffix: '.min'}))
    .pipe(cssnano({discardComments: {removeAll: true}}))
    .pipe(concat('webapp.min.css'))
    .pipe(gulp.dest(basePaths.target + 'css/'));
});

// helper cleancss
gulp.task('cleancss', function() {
  return gulp.src(basePaths.temp + 'css/*.min.css', { read: false })
    .pipe(rimraf());
});

// gulp scripts
gulp.task('concat-js', function() {
  gulp.src([
        basePaths.temp + 'js/1jquery/jquery.js',
        basePaths.temp + 'js/2tether/tether.js',
        basePaths.temp + 'js/3bootstrap/bootstrap.js',
        basePaths.temp + 'js/4bootstrap-multiselect/bootstrap-multiselect.js',
        basePaths.temp + 'js/4bootstrap-multiselect/bootstrap-multiselect-collapsible-groups.js',
        basePaths.temp + 'js/5seiyria-bootstrap-slider/bootstrap-slider.js',
        basePaths.temp + 'js/6leaflet/leaflet.js',
        basePaths.temp + 'js/7leaflet-vector-markers/leaflet-vector-markers.js',
				basePaths.temp + 'js/8livesearch/livesearch.js',
        basePaths.temp + 'js/9webapp/webapp.js'
      ])
    .pipe(concat('webapp.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(basePaths.target + './js/'));
});

// helper cleanjs
gulp.task('cleanjs', function() {
  return gulp.src(basePaths.temp + 'js/**/*.min.js', { read: false }) 
    .pipe(rimraf());
});


gulp.task('copy-assets', function(cb) {

  /********** JS **********/
  // jQuery
  gulp.src(basePaths.bower + 'jquery/dist/*.js')
    .pipe(gulp.dest(basePaths.temp + '/js/1jquery'));
  
  // Tether
  gulp.src(basePaths.bower + 'tether/dist/js/*.js')
    .pipe(gulp.dest(basePaths.temp + '/js/2tether'));
  
  // Bootstrap
  gulp.src(basePaths.bower + 'bootstrap/dist/js/bootstrap.js')
    .pipe(gulp.dest(basePaths.temp + '/js/3bootstrap'));
  
  // Bootstrap Multiselect
  gulp.src(basePaths.bower + 'bootstrap-multiselect/dist/js/*.js')
    .pipe(gulp.dest(basePaths.temp + '/js/4bootstrap-multiselect'));
    
  // Bootstrap Slider
  gulp.src(basePaths.bower + 'seiyria-bootstrap-slider/dist/bootstrap-slider.js')
    .pipe(gulp.dest(basePaths.temp + '/js/5seiyria-bootstrap-slider'));
    
  // Leaflet
  gulp.src(basePaths.bower + 'leaflet/dist/*.js')
    .pipe(gulp.dest(basePaths.temp + '/js/6leaflet/'));
  
  // Leaflet Vector Markers
  gulp.src(basePaths.bower + 'leaflet.vector-markers/dist/leaflet-vector-markers.js')
    .pipe(gulp.dest(basePaths.temp + '/js/7leaflet-vector-markers/'));
  
  // LiveSearch
  gulp.src(basePaths.assets + 'js/livesearch.js')
    .pipe(gulp.dest(basePaths.temp + 'js/8livesearch/'));
		
  // Own JS Assets
  gulp.src(basePaths.assets + 'js/webapp.js')
    .pipe(gulp.dest(basePaths.temp + 'js/9webapp/'));

  /********** SASS **********/
  
  // Base
  gulp.src(basePaths.assets + 'base/base.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/'));
    
  // Bootstrap
  gulp.src(basePaths.bower + 'bootstrap/scss/**/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/bootstrap/'));
  
  // Bootstrap Multiselect
  gulp.src(basePaths.bower + 'bootstrap-multiselect/dist/css/bootstrap-multiselect.css')
    .pipe(rename('bootstrap-multiselect.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/bootstrap-multiselect/'));
    
  // Bootstrap Slider
  gulp.src(basePaths.bower + 'seiyria-bootstrap-slider/src/sass/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/seiyria-bootstrap-slider/'));
    
  // Leaflet
  gulp.src(basePaths.bower + 'leaflet/dist/leaflet.css')
    .pipe(rename('leaflet.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/leaflet/'));
	
  // Leaflet Vector Markers
  gulp.src(basePaths.bower + 'leaflet.vector-markers/dist/leaflet-vector-markers.css')
    .pipe(rename('leaflet-vector-markers.scss'))
    .pipe(gulp.dest(basePaths.temp + 'sass/leaflet-vector-markers/'));
  
  // Font Awesome
  gulp.src(basePaths.bower + 'fontawesome/scss/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/fontawesome/'));

  gulp.src(basePaths.assets + 'sass/**/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/webapp/'));
  
  
  /********** Fonts **********/
  
  // Google Fonts
  gulp.src(basePaths.assets + 'fonts.list')
		.pipe(googleWebFonts({
      fontsDir: basePaths.target + 'fonts/google-fonts/',
      cssDir: basePaths.temp + 'pre-sass/google-fonts/',
      cssFilename: 'google-fonts.scss'
    }))
		.pipe(gulp.dest('./'));
  
  gulp.src(basePaths.temp + 'pre-sass/google-fonts/google-fonts.scss')
    .pipe(replace('webapp', ''))
    .pipe(gulp.dest(basePaths.temp + 'sass/google-fonts/'));
    
  // Font Awesome Fonts
  gulp.src(basePaths.bower + 'fontawesome/fonts/**/*.{ttf,woff,woff2,eof,svg}')
    .pipe(gulp.dest(basePaths.target + 'fonts/fontawesome/'));

    
  /********** Images **********/
  
  // Leaflet Images
  gulp.src(basePaths.bower + 'leaflet/dist/images/*')
    .pipe(gulp.dest(basePaths.target + 'images/leaflet/'));
  
  // Mapbox Images
  gulp.src(basePaths.bower + 'mapbox.js/images/*')
    .pipe(gulp.dest(basePaths.target + 'images/mapbox.js/'));
});

gulp.task('copy-assets-webapp-css', [], function() {
  gulp.src(basePaths.assets + 'sass/**/*.scss')
    .pipe(gulp.dest(basePaths.temp + 'sass/webapp/'));
});

gulp.task('copy-assets-webapp-js', function() {
  // Own JS Assets
  return gulp.src(basePaths.assets + 'js/webapp.js')
    .pipe(gulp.dest(basePaths.temp + 'js/9webapp/'));
});
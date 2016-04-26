var terrariumHome = angular.module('terrarium.home', ['ngRoute']);

terrariumHome.config(function($routeProvider) {

    $routeProvider.
        when('/home', {
            templateUrl: 'partials/main/home.html',
            controller: 'HomeController'
        }).
        when('/about', {
            templateUrl: 'partials/main/about.html',
            controller: 'AboutController'
        }).
        when('/tools', {
            templateUrl: 'partials/tools/home.html',
            controller: 'ToolController'
        }).
        otherwise({redirectTo: '/home'});
});

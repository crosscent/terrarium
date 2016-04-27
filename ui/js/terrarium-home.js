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
        otherwise({redirectTo: '/home'});
});

terrariumHome.controller("HomeController", function($scope) {
    $scope.hello = "Hello";
});

terrariumHome.controller("AboutController", function($scope) {

});

var terrariumTools = angular.module('terrarium.tools', ['ngRoute']);

terrariumTools.config(function($routeProvider) {

    $routeProvider.
        when('/tools', {
            templateUrl: 'partials/tools/home.html',
            controller: 'ToolController'
        }).
        when('/tools/pot_calculation', {
            templateUrl: 'partials/tools/pot_calculation.html',
            controller: 'ToolPotCalculationController'
        })
});

terrariumTools.controller("ToolController", function($scope) {

});

terrariumTools.controller("ToolPotCalculationController", function($scope) {

});

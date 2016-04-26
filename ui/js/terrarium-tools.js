var terrariumTools = angular.module('terrarium.tools', ['ngRoute']);

terrariumTools.config(function($routeProvider) {

    $routeProvider.
        when('/tools/pot_calculation', {
            templateUrl: 'partials/tools/pot_calculation.html',
            controller: 'ToolPotCalculationController'
        })
});


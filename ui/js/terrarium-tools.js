var terrariumTools = angular.module('terrarium.tools', ['ngRoute', 'ngResource']);

terrariumTools.config(function($routeProvider) {

    $routeProvider.
        when('/tools', {
            templateUrl: 'partials/tools/home.html',
            controller: 'ToolController'
        }).
        when('/tools/pot_calculation', {
            templateUrl: 'partials/tools/pot_calculation.html',
            controller: 'ToolController'
        })
});

terrariumTools.factory('api', function($resource) {
    return {
        rectangular_pot: $resource('/api/calculation/rectangular_pot\\/',
            {
                pot_length: $resource.pot_length,
                pot_width: $resource.pot_width,
                seed_radius: $resource.seed_radius            
            },
            {
                get: {method: 'GET'}
            }),
        circular_pot: $resource('/api/calculation/circular_pot\\/',
            {
                pot_radius: $resource.pot_radius,
                seed_radius: $resource.seed_radius            
            }, 
            {
                get: {method: 'GET'}
            }),
    };

});

terrariumTools.controller("ToolController", function($scope, api) {
    $scope.getFormData = function(){
        if ($scope.pot_type == 'rectangular') {
            return {pot_width: $scope.pot_width,
                    pot_length: $scope.pot_length,
                    seed_radius: $scope.seed_radius};
        } else if ($scope.pot_type == 'circular') {
            return {pot_radius: $scope.pot_radius,
                    seed_radius: $scope.seed_radius};
        }
    };

    $scope.get_pot_image = function() {
        if ($scope.pot_type == 'rectangular') {
            result = api.rectangular_pot.get($scope.getFormData());
        } else if ($scope.pot_type == 'circular') {
            result = api.circular_pot.get($scope.getFormData());
        }
        result.$promise.then(function(data){
            $scope.cluster_count = data.cluster_count;
            $scope.cluster_image = data.image;
        })
    };
});

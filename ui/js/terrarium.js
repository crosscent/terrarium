'use strict';

angular.module("terrarium", [])

.controller("HelloController", function($scope) {
    $scope.helloTo = {};
    $scope.helloTo.title = "AngularJS";
});

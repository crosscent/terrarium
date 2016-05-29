'use strict';

var terrarium = angular.module("terrarium",
                               ['terrarium.auth',
                                'terrarium.d3',
                                'terrarium.home',
                                'terrarium.tools',
                                'ui.bootstrap']);

terrarium.controller('menuCtrl', function($scope, $location) {
    $scope.menuLinks = [{
        title: 'Home',
        url: 'home',
    }, {
        title: 'About',
        url: 'about',
    }, {
        title: 'Tools',
        url: 'tools',
    },];

    $scope.menuClass = function (page_url) {
        var currentRoute = $location.path().substring(1) || 'home';
        return page_url == currentRoute ? 'active': '';
    }
});

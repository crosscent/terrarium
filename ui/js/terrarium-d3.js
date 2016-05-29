'use strict';

var terrariumD3 = angular.module('terrarium.d3', []);

terrariumD3.factory('d3Service', function($document, $q, $rootScope){
    var d = $q.defer();
    function onScriptLoad() {
        $rootScope.$apply(function() {d.resolve(window.d3);});
    }

    var scriptTag = $document[0].createElement('script');
    scriptTag.type = 'text/javascript';
    scriptTag.async = true;
    scriptTag.src = 'http://d3js.org/d3.v3.min.js';
    scriptTag.onreadystatechange = function () {
        if (this.readyState == 'complete')
            onScriptLoad();
    }

    scriptTag.onload = onScriptLoad;
    
    var s = $document[0].getElementsByTagName('body')[0];
    s.appendChild(scriptTag);

    return {
        d3: function() {return d.promise;}
    };
});

terrariumD3.config(function($routeProvider) {

    $routeProvider.
        when('/graph', {
            templateUrl: 'partials/d3/plants.html',
            })
});

terrariumD3.directive('barChart', ['d3Service', function(d3Service) {
    return {
        link: function(scope, element, attrs) {
              d3Service.d3().then(function(d3) {
              });
        }
    }
}]);

terrariumD3.directive('d3Bars', function(d3Service, $window) {
    return {
        restrict: 'EA', 
        scope: {},
        link: function(scope, ele, attrs) {
            d3Service.d3().then(function(d3) {
                var margin = parseInt(attrs.margin) || 20,
                    barHeight = parseInt(attrs.barHeight) || 20,
                    barPadding = parseInt(attrs.barPadding) || 5;

                var svg = d3.select(ele[0]).append('svg').style('width', '100%');

                window.onresize = function() {
                    scope.$apply();
                }

                scope.data = [
                    {name: 'Greg', score: 98},
                    {name: 'Mary', score: 96},
                    {name: 'Brad', score: 75},
                    {name: 'Cath', score: 48}
                ];

                scope.$watch(function() {
                    return angular.element($window)[0].innerWidth;
                }, function() {
                    scope.render(scope.data);
                });

                scope.render = function(data) {
                    svg.selectAll('*').remove();

                    if (!data) return;

                    var width = d3.select(ele[0]).node().offsetWidth - margin,
                        height = scope.data.length * (barHeight + barPadding),
                        color = d3.scale.category20(),
                        xScale = d3.scale.linear()
                                    .domain([0, d3.max(data, function(d) {
                                        return d.score;
                                    })])
                                    .range([0, width]);

                    svg.attr('height', height);

                    svg.selectAll('rect')
                       .data(data).enter()
                       .append('rect')
                       .attr('height', barHeight)
                       .attr('width', 140)
                       .attr('x', Math.round(margin/2))
                       .attr('y', function(d, i) {
                           return i * (barHeight + barPadding);
                       })
                       .attr('fill', function(d) {return color(d.score);})
                       .transition()
                       .duration(1000)
                       .attr('width', function(d) {
                           return xScale(d.score);
                       });
                }
            });
        }};
});


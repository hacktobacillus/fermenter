(function() {
angular.module("kettleApp")
.directive("beerCard",function() {

    function link(scope,element,attrs) {
        
    }

    return {
        link: link,
        templateUrl: '/static/html/beerCardTemplate.html',
        scope: {
            beer: '=',
            upVote: '&',
            downVote: '&',
        }
    }
});
})()

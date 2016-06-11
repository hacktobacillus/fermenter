(function() {
angular.module("kettleApp")
.controller("kettleCtrl",function($scope,$http) {
    $scope.model = {
        beer_list: []
    }

    

    $scope.like_beers = [];
    $scope.dislike_beers = [];
    $scope.postBeers = postBeers;
    $scope.downVoteBeer = downVoteBeer;
    $scope.upVoteBeer = upVoteBeer;


    $http.get('/kettle/beer_list').then(
        function(data) {
            $scope.model.beer_list = data.data.result;
        },
        function () {}
    );


    function voteBeer(beer,a,b) {
        // return if this beer has been voted on.
        var beer_exists = false;
        for (var i in a) {
            var bid = a[i];
            if (beer.id == bid) {
                beer_exists = true;
                break
            }
        }
        if (!beer_exists) {
            a.push(beer.id);
        }

        // Make sure it's not in dislike beers.
        for (var i in b) {
            var bid  = b[i];
            // remove it if present
            if (beer.id == bid) {
                b.splice(i,1);
                beer.voted_on = false;
                return;
            }
        }
        beer.voted_on = true;
}

    function reset() {
        $scope.dislike_beers = [];
        $scope.like_beers = [];
    }

    function upVoteBeer(beer) {
        voteBeer(beer,$scope.like_beers,$scope.dislike_beers);
        console.log([$scope.like_beers,$scope.dislike_beers]);
    }

    function downVoteBeer(beer) {
        voteBeer(beer,$scope.dislike_beers,$scope.like_beers);
        console.log([$scope.like_beers,$scope.dislike_beers]);
     }


    function postBeers() {
        $http.post('/kettle/crunch',{like_ids:$scope.like_beers,dislike_ids:$scope.dislike_beers}).then(
        function (data) { 
            $scope.results = data.data.result;
            console.log($scope.results);
            $('#myModal').modal('show');
        },
        function () { 
            alert('failed');
        });
    }
});
})()

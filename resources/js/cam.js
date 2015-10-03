angular.module("cam", ["ui.router", "ui.bootstrap",  "angular-loading-bar"])
    .run(["$rootScope", "$state", "$stateParams", "$http", "Session", function($rootScope, $state, $stateParams, $http, Session) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.Session = Session;
        $http.get("api/user").then(function(response) {Session.set(response.data);});
    }])
    .config(["$urlRouterProvider", "$stateProvider", function($urlRouterProvider, $stateProvider) {
        $urlRouterProvider.otherwise("/pacientes/ultimos");
        $stateProvider
            .state("patients-last", {
                url: "/pacientes/ultimos",
                templateUrl: "templates/patients-last.html"
            })
            .state("patient-new", {
                url: "/paciente/nuevo",
                templateUrl: "templates/patient-new.html"
            })
            .state("patient-view", {
                url: "/paciente/{id:int}",
                templateUrl: "templates/patient-view.html"
            });
    }])
    .service("Session", function() {
        this.ROLE_ADVISOR = "advisor";
        this.user = null;
        this.roles = [];
        this.set = function(obj) {
            this.user = obj.user;
            this.roles = obj.roles;
        }
        this.hasRole = function(role) {return this.roles.indexOf(role) >= 0;}
    })
    .controller("PatientsLastController", ["$scope", "$http", function($scope, $http) {
        $scope.patients = [];
        $http.get("api/patients/last").then(function(response) {$scope.patients = response.data;});
    }])
    .controller("PatientNewController", ["$scope", "$http", "$filter", function($scope, $http, $filter) {
        $scope.processing = false;
        $scope.patient = {
            firstname: null,
            middlename: null,
            surname: null,
            birthdate: null,
            nationality: null
        };
        $scope.birthdatePicker = {
            isVisible: false,
            minDate: new Date(1900, 1, 1),
            maxDate: new Date(),
            options: {startingDay: 1}
        };
        $scope.errors = {};
        $scope.save = function() {
            $scope.processing = true;
            var patient = angular.merge({}, $scope.patient);
            patient.birthdate = $filter("date")(patient.birthdate, "yyyy-MM-dd");
            $http.post("api/patient", patient).then(function(response) {
                $scope.errors = {};
                $scope.processing = false;
                $scope.$state.go("patient-view", response.data)
            }, function(response) {
                $scope.errors = response.data;
                $scope.processing = false;
            });
        }
    }])
    .controller("PatientViewController", ["$scope", "$http", function($scope, $http) {
        $http.get("api/patient/" + $scope.$stateParams.id).then(function(response) {$scope.patient = response.data;});
    }]);

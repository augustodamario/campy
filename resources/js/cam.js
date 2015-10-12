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
                templateUrl: "templates/patients-last.html",
                controller: "PatientsLastController"
            })
            .state("patient-new", {
                url: "/paciente/nuevo",
                templateUrl: "templates/patient-profile.html",
                controller: "PatientProfileController"
            })
            .state("patient-view", {
                url: "/paciente/{id:int}",
                templateUrl: "templates/patient-view.html",
                controller: "PatientViewController"
            })
            .state("patient-edit", {
                url: "/paciente/{id:int}/modificar",
                templateUrl: "templates/patient-profile.html",
                controller: "PatientProfileController"
            });
    }])
    .service("Session", function() {
        this.ROLE_ADVISOR = "advisor";
        this.ROLE_SYSTEM_ADMINISTRATOR = "system administrator";
        this.set = function(obj) {angular.extend(this, obj);}
        this.hasRole = function(role) {return !!this.roles && this.roles.indexOf(role) >= 0;}
    })
    .controller("AppController", ["$scope", function($scope) {
        $scope.patientLinks = [];
        $scope.addPatientLink = function(id, name) {
            if (!$scope.patientLinks.some(function(p) {return p.id === id;})) {
                $scope.patientLinks.push({id: id, name: name});
            }
        }
        $scope.removePatientLink = function(num) {
            $scope.patientLinks.splice(num, 1);
        }
    }])
    .controller("PatientsLastController", ["$scope", "$http", function($scope, $http) {
        $scope.patients = [];
        $http.get("api/patients/last").then(function(response) {$scope.patients = response.data;});
    }])
    .controller("PatientProfileController", ["$scope", "$http", "$filter", function($scope, $http, $filter) {
        var url = "api/patient";
        $scope.patient = {};
        if ($scope.$stateParams.id) {
            url += "/" + $scope.$stateParams.id;
            $http.get(url).then(function(response) {$scope.patient = response.data;});
        }
        $scope.processing = false;
        $scope.birthdatePicker = {
            isVisible: false,
            minDate: new Date(1900, 0, 1),
            maxDate: new Date(),
            options: {startingDay: 1}
        };
        $scope.errors = {};
        $scope.cancel = function() {
            if ($scope.$stateParams.id) {
                $scope.$state.go("patient-view", {id: $scope.$stateParams.id});
            } else {
                $scope.$state.go("patients-last");
            }
        }
        $scope.save = function() {
            $scope.processing = true;
            var patient = angular.merge({}, $scope.patient);
            patient.birthdate = $filter("date")(patient.birthdate, "yyyy-MM-dd");
            $http.post(url, patient).then(function(response) {
                $scope.errors = {};
                $scope.processing = false;
                $scope.$state.go("patient-view", response.data);
            }, function(response) {
                $scope.errors = response.data;
                $scope.processing = false;
            });
        }
    }])
    .controller("PatientViewController", ["$scope", "$http", function($scope, $http) {
        $http.get("api/patient/" + $scope.$stateParams.id).then(function(response) {
            var patient = $scope.patient = response.data;
            $scope.$parent.addPatientLink(patient.id, patient.firstname + " " + patient.surname);
        });
    }]);

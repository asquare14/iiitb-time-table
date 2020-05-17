
$(function () {
    $("#search-bar").autocomplete({
        source: "/search/",
        // minLength: 3,
    });
}
);

function clearTT() {
    for (var i = 0; i < 5; ++i) {
        for (var j = 0; j < 9; ++j) {
            $('#' + i.toString() + j.toString()).removeClass('border border-danger');
            $('#' + i.toString() + j.toString()).removeClass('table-danger');
            $('#' + i.toString() + j.toString()).removeClass('table-clash');
            $('#' + i.toString() + j.toString()).html('');
        }
    }
    clearSelected();
    console.log("oops")
}

function addToCalendar(){
    var timetable = [];
    var todaysDate = new Date();
    var todaysDay = todaysDate.getDay();
    if(todaysDay == 0)
        todaysDay = 6;
    else
        todaysDay = todaysDay - 1;
    for (var i = 0; i < 5; ++i) {
        for (var j = 0; j < 9; ++j) {
            if($('#' + i.toString() + j.toString()).hasClass('table-danger') || $('#' + i.toString() + j.toString()).hasClass('table-clash')){
                var curr = [];
                curr.push($('#' + i.toString() + j.toString()).html())
                var d = new Date();
                var numberOfDaysToAdd = 0;
                if(i < todaysDay){
                    numberOfDaysToAdd = i + 7 - todaysDay;
                }
                else{
                    numberOfDaysToAdd = i - todaysDay;
                }
                d.setDate(d.getDate() + numberOfDaysToAdd);
                var ye = d.getFullYear();
                var mo = d.getMonth() + 1;
                var da = d.getDate();
                var start = '' + ye.toString() + '-' + mo.toString() + '-' + da.toString() + ' ';
                var end = start;
                if(j == 0){
                    start = start + '08:00:00';
                    end = end + '08:00:55';
                }
                else if(j == 1){
                    start = start + '09:00:00';
                    end = end + '09:00:55';
                }
                else if(j == 2){
                    start = start + '10:00:00';
                    end = end + '10:00:55';
                }
                else if(j == 3){
                    start = start + '11:00:00';
                    end = end + '11:00:55';
                }
                else if(j == 4){
                    start = start + '12:00:00';
                    end = end + '12:00:55';
                }
                else if(j == 5){
                    start = start + '14:00:00';
                    end = end + '14:00:55';
                }
                else if(j == 6){
                    start = start + '15:00:00';
                    end = end + '15:00:55';
                }
                else if(j == 7){
                    start = start + '16:00:00';
                    end = end + '16:00:55';
                }
                else if(j == 8){
                    start = start + '17:00:00';
                    end = end + '17:00:55';
                }
                curr.push(start)
                curr.push(end)
                timetable.push(curr)
            }
        }
    }
    console.log(timetable)
}

function sdCallback(data, id, course) {
    $('#details-div').html("");
    if (typeof data['Name'] !== "undefined") {
        if (id === undefined) {
            var details = "";
            details += "<b>Name: </b>" + data['Name'] + " <br>";
            courseData = data['Data'];
            for (var key in courseData) {
                details += "<b>" + key + ": </b>" + courseData[key] + " <br>";
            }
            $('#details-div').html(details);

            for (var slot in courseData['Slot']) {
                $('#' + courseData['Slot'][slot]).addClass('border border-danger');
                if($('#' + courseData['Slot'][slot]).hasClass('table-danger')){
                    $('#' + courseData['Slot'][slot]).removeClass('table-danger');
                    $('#' + courseData['Slot'][slot]).addClass('table-clash');
                    
                }
                else{
                    $('#' + courseData['Slot'][slot]).addClass('table-danger');
                    $('#' + courseData['Slot'][slot]).html(data['Name'].split(':')[0])
                }
            }
        }
        else {
            parentList = document.getElementById(id);
            var item = document.createElement('li');
            item.className = "course";
            item.setAttribute("onclick", "searchData(this)");
            item.innerHTML = course;
            parentList.appendChild(item);
        }
    }
}

function clearSelected() {
    $('.active').removeClass('active');
}


function searchData(q = $("#search-bar").val(), id = undefined) {
    var searchString = "";
    if (typeof q !== "string") {
        searchString = q.innerHTML; // Get list item's name
        q.className += ' active';
    }
    else {
        searchString = q;
    }
    $.post("/ajax/",
        {
            "query": searchString
        },
        function (data) {
            sdCallback(data, id, searchString);
        },
        "json"
    );
}

$("#search-but").click(searchData);
$("#search-bar").on('keypress', function (e) {
    if (e.which === 13) {
        $(this).attr("disabled", "disabled");
        searchData();
        $(this).removeAttr("disabled");
    }
});

function loadMinor() {
    $.get("/minor/", function (data) {
        minorDiv = document.getElementById('minor-div');
        var jdata = JSON.parse(data);
        for (var i in jdata) {
            var minor = jdata[i];

            // Create heading
            var heading = document.createElement('h3');
            heading.className = "accordion";
            heading.innerHTML = "<i data-feather='chevron-down'></i>" + minor['Name'];
            heading.addEventListener(
                'click',
                function (e) {
                    var elem = $(e.target)[0].nextElementSibling;
                    $(elem).toggleClass('open');
                    e.target.removeChild(e.target.childNodes[0]);
                    innerHTML = e.target.innerHTML;
                    if ($(elem).hasClass('open')) {
                        e.target.innerHTML = "<i data-feather='chevron-right'></i>" + innerHTML;
                    } else {
                        e.target.innerHTML = "<i data-feather='chevron-down'></i>" + innerHTML;
                    }
                    feather.replace();
                } //onclick displays course list of each dept
                , false
            )
            minorDiv.appendChild(heading);

            // Create list
            var list = document.createElement('ul');
            list.className = "panel";
            list.id = i.toString();

            // Populate list
            for (var j in minor['Courses']) {
                course = minor['Courses'][j];
                searchData(course, i.toString());
            }

            // Add to page
            minorDiv.appendChild(list);
        }
        new SimpleBar(minorDiv, { autoHide: false });
    }).promise().done(
        () => {
            feather.replace()
        }
    );
}

loadMinor();
setTimeout(
    () => {
        new SimpleBar($('.ui-menu')[0]);

    }, 1000

)

function toggle(el) {
    element = $(el);
    if (element.hasClass('table-danger')){
        element.removeClass('table-danger');
    }
    else{
        element.addClass('table-danger');
    }
}

$('#timet td').attr('onclick', 'toggle(this)');

function readICS() {
    var file = document.getElementById('file-in').files[0];
    if (file) {
        $('#timet td').removeClass('table-clash');

        var reader = new FileReader();
        reader.onload = function (e) {
            var content = e.target.result;
            var slots = content.split('DTSTART;TZID=Asia/Kolkata;VALUE=DATE-TIME:');
            for (i in slots) {
                var slot = slots[i];
                if (i > 0) {
                    var hour = parseInt(slot.substring(9, 11));
                    var year = parseInt(slot.substring(0, 4));
                    var month = parseInt(slot.substring(4, 6)) - 1;
                    var date = parseInt(slot.substring(6, 8));

                    var d = new Date(year, month, date);

                    var day = d.getDay() - 1;

                    var duration = parseInt(slot.substring(28, 29));

                    if (hour < 14)
                        hour -= 8;
                    else
                        hour -= 9;

                    for (var i = 0; i < duration; ++i) {
                        var id = day.toString() + (hour + i).toString();
                        $('#' + id).addClass('table-clash');
                    }

                }
            }
        }

        reader.readAsText(file);
    }
}
$(function () {    
    (function ($) {
        $.fn.prettyCalendar = function (options) {
            
            var settings = $.extend({
                customDay: new Date(),
                color: '#65c2c0',
            }, options);
            
            var dayNames = {};
            var monthNames = {};
            var AddEvent = {};
            var AllDay = {};
            var TotalEvents = {};
            var Event = {};
            dayNames = new Array('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun');
            monthNames = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'); 
            AddEvent = 'Add New Event';
            AllDay = 'All Day';
            TotalEvents = 'Total Events in This Month: ';
            Event = 'Event(s)';

            XHRresponse = {"count": 7, "dates": [1, 2, 3, 7, 15, 21, 24]};
            JSONevents =    {
                                event0: {startTime: {hour:12, minute:30},   
                                        endTime: {hour:14, minute:0},
                                        name:"MyEvent",
                                        description:""
                                        //id
                                    },
                                    
                                event1: {startTime: {hour:8, minute:30},
                                        endTime: {hour:20, minute:15},
                                        name:"MyEvent1",
                                        description:""
                                        //id
                                    },
                                    
                                event2: {startTime: {hour:2, minute:30},
                                        endTime: {hour:20, minute:15},
                                        name:"MyEvent2",
                                        description:""
                                        //id
                                    }
                                };
            
            var $this = $(this);
            var div = function (e, classN) {
                return $(document.createElement(e)).addClass(classN);
            };

            var clockHour = [];
            var clockMin = [];
            for (var i=0;i<24;i++ ){
                clockHour.push(div('div', 'option').text(i))
            }
            for (var i=0;i<59;i+=5 ){
                clockMin.push(div('div', 'option').text(i))
            }
            
            $this.append(
                div('div', 'wood-bottom'), 
                div('div', 'prettyCalendar-wood').append(
                    div('div', 'close-button'),
                    div('div', 'prettyCalendar-pages').append(
                        div('div', 'pages-bottom'),
                        div('div', 'header').css('background-color', settings.color).append(
                            div('a', 'prv-m'),
                            div('h1'),
                            div('a', 'nxt-m'),
                            div('div', 'day-names')
                        ),
                        div('div', 'total-bar').html( TotalEvents + '<b style="color: '+settings.color+'"></b>'),
                        div('div', 'days')
                    ),
                    div('div', 'add-event').append(
                        div('div', 'add-new').append(
                            '<input type="text" placeholder="' + AddEvent + '" value="' + AddEvent + '" />',
                            div('div', 'submit'),
                            div('div', 'clear'),
                            div('div', 'add-time').append(
                                div('div', 'disabled'),
                                div('div', 'select').addClass('hour').css('background-color', settings.color).append(
                                    div('span').text('00'),
                                    div('div', 'dropdown').append(clockHour)
                                ),
                                div('div', 'left').append(':'),
                                div('div', 'select').addClass('min').css('background-color', settings.color).append(
                                    div('span').text('00'),
                                    div('div', 'dropdown').append(clockMin)
                                )
                            ),
                            div('div', 'all-day').append(
                                div('fieldset').attr('data-type','disabled').append(
                                    div('div', 'check').append(
                                        div('span', '')
                                    ),
                                    div('label').text(AllDay)
                                )
                            ),
                            div('div', 'clear')
                        ),
                        div('div', 'events').append(
                            div('h3','').append(
                                div('span', '').html('<b></b> ' + Event)
                            ),
                            div('div', 'gradient-wood'),
                            div('div', 'events-list')
                        )
                    )
                )
            );
            
            for (var i = 0; i < 42; i++) {
                $this.find('.days').append(div('div', 'day'));
            }
            
            for (var i = 0; i < 7; i++) {
                $this.find('.day-names').append(div('h2').text(dayNames[i]));
            }

            var d = new Date(settings.customDay);
            var year = d.getFullYear();
            var date = d.getDate();
            var month = d.getMonth();
            
            var isLeapYear = function(year1) {
                var f = new Date();
                f.setYear(year1);
                f.setMonth(1);
                f.setDate(29);
                return f.getDate() == 29;
            };
        
            var feb;
            var febCalc = function(feb) { 
                if (isLeapYear(year) === true) { feb = 29; } else { feb = 28; } 
                return feb;
            };
            var monthDays = new Array(31, febCalc(feb), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);

            function calcMonth() {

                monthDays[1] = febCalc(feb);
                
                var weekStart = new Date();
                weekStart.setFullYear(year, month, 0);
                var startDay = weekStart.getDay();  
                
                $this.find('.header h1').html(monthNames[month] + ' ' + year);
        
                $this.find('.day').html('&nbsp;');
                $this.find('.day').removeClass('this-month');
                for (var i = 1; i <= monthDays[month]; i++) {
                    startDay++;
                    $this.find('.day').eq(startDay-1).addClass('this-month').attr('data-date', i+'/'+(month+1)+'/'+year).html(i);
                }
                if ( month == d.getMonth() ) {
                    $this.find('.day.this-month').removeClass('today').eq(date-1).addClass('today').css('color', settings.color);
                } else {
                    $this.find('.day.this-month').removeClass('today').attr('style', '');
                }
                
                $this.find('.added-event').each(function(i){
                    $(this).attr('data-id', i);
                    $this.find('.this-month[data-date="' + $(this).attr('data-date') + '"]').append(
                        div('div','event-single').attr('data-id', i).append(
                            div('p','').text($(this).attr('data-title'))
                            ),
                            div('div','details').append(
                                div('div', 'clock').text($(this).attr('data-time')),
                                div('div', 'erase')
                            )
                        );
                    $this.find('.day').has('.event-single').addClass('have-event').prepend(div('i',''));
                });
                
                calcTotalDayAgain();  
                
            }
            
            calcMonth();
            queryEventsYM(year,month);
            function queryEventsYM(year,month) {
                $.ajax({
                    type: 'GET',
                    url: "/events/" + year + "/" + (month + 1) + "/",
                    success: function(data){
                        $('.total-bar b').text(data.count);
                        for(i = 0; i < data.dates.length; i++) {
                            var match = $('.day.this-month').filter(function(){
                                var date = $(this).attr("data-date").split("/");
                                var day = date[0];
                                var month = date[1];
                                if(date[0] == data.dates[i] && date[1] == month)
                                    return true;
                            });
                            match.addClass('have-event').prepend(div('i','')).append(div('div','event-single'));
                        }
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }

            function dispatchEvent(eventSingle0, event){        
                var e0 = JSON.parse(JSON.stringify(event));
                var e0start = JSON.parse(JSON.stringify(e0.startTime));
                var e0startOut = e0start.hour.toString().concat(':').concat(e0start.minute.toString());
                //var e0end = JSON.parse(JSON.stringify(e0.endTime));
                //e0endOut = e0end.hour.toString().concat(':').concat(e0end.minute.toString());
                eventSingle0.find('p').text(e0.name) ;
                eventSingle0.find('.details').find('.clock').text(e0startOut) ;
                $this.find('.add-event').show().find('.events-list').append(createEventHTML(e0.name, e0startOut, e0.id));
                // $this.find('.events-list').append(createEventHTML(e0.name, e0startOut));
            }

            function createEventHTML(title, time, eventId){
                var dataId = parseInt($this.find('.total-bar b').text());
                
                eventHTML = (
                    div('div','event-single').attr('data-id', dataId).attr('data-eventid', eventId).append(
                        div('p','').text(title),
                        div('div', 'volunteer').append(
                            div('div', 'volunteerText').text('Volunteer?'),
                            div('div', 'volunteerIcon')
                        ),
                        div('div','details').append(
                            div('div', 'clock').text(time),
                            div('div', 'erase')
                        )
                    )
                );
                dataId++;
                return(eventHTML);
            }

            var arrows = new Array ($this.find('.prv-m'), $this.find('.nxt-m'));
            var dropdown = new Array ($this.find('.add-time .select span'), $this.find('.add-time .select .dropdown .option'), $this.find('.add-time .select'));
            var allDay = new Array ('.all-day fieldset[data-type="disabled"]', '.all-day fieldset[data-type="enabled"]');
            var $close = $this.find('.prettyCalendar-wood > .close-button');
            var $erase = $this.find('.event-single .erase');
            $this.find('.prettyCalendar-pages').css({'width' : $this.find('.prettyCalendar-pages').width() });
            $this.find('.events').css('height', ($this.height()-197) );
            $this.find('.select .dropdown .option').hover(function() {
                $(this).css('background-color', settings.color); 
            }, function(){
                $(this).css('background-color', 'inherit'); 
            });
            var prettyCalendarWoodW = $this.find('.prettyCalendar-wood').width();
            var woodBottomW = $this.find('.wood-bottom').width();

            function calcScroll() {
                if ( $this.find('.events-list').height() < $this.find('.events').height() ) { $this.find('.gradient-wood').hide(); $this.find('.events-list').css('border', 'none') } else { $this.find('.gradient-wood').show(); }
            }
            
            function calcTotalDayAgain() {
                var eventCount = $this.find('.this-month .event-single').length;
                $this.find('.total-bar b').text(eventCount);
                $this.find('.events h3 span b').text($this.find('.events .event-single').length)
            }
            
            function prevAddEvent() {
                $this.find('.day').removeClass('selected').removeAttr('style');
                $this.find('.today').css('color', settings.color);
                $this.find('.add-event').hide();
                $this.children('.prettyCalendar-wood').animate({'width' : prettyCalendarWoodW}, 200);
                $this.children('.wood-bottom').animate({'width' : woodBottomW}, 200);
                $close.hide();
            }
            
            arrows[1].on('click', function () {
                if ( month >= 11 ) {
                    month = 0;
                    year++;
                } else {
                    month++;   
                }
                calcMonth();
                queryEventsYM(year,month);
                prevAddEvent();
            });
            arrows[0].on('click', function () {
                dayClick = $this.find('.this-month');
                if ( month === 0 ) {
                    month = 11;
                    year--;
                } else {
                    month--;   
                }
                calcMonth();
                queryEventsYM(year,month);
                prevAddEvent();
            });
            
            $this.on('click', '.volunteer', function(){
                var self = $(this);
                $.ajax({
                    type: 'GET',
                    data: self.parent().attr("data-eventid"),
                    url: "/events/signup/",
                    success: function(){
                        self.find('.volunteerText').text('Volunteering!');
                        console.log('Success!');
                    },
                    error: function() {
                        self.find('.volunteerText').text('Problem occured.');
                        console.log('Success!');
                    }
                });
            });

            $this.on('click', '.this-month', function () {
                var eventSingle = $(this).find('.event-single')
                $this.find('.events .event-single').remove();
                prevAddEvent();
                $(this).addClass('selected').css({'background-color': settings.color});
                var date = $(this).attr("data-date").split("/");
                var selectedDay = date[0];
                var selectedMonth = date[1];
                var selectedYear = date[2];
                
                $.ajax({
                    type: 'GET',
                    url: "/events/" + selectedYear + "/" + selectedMonth + "/" + selectedDay + "/",
                    success: function(data){
                        var JSONarray = [] ;
                        $.each(data, function(){
                            var e0 = JSON.parse(JSON.stringify(this));
                            JSONarray.push(e0);
                        });
                        $.each(JSONarray, function(index, dispatchedEvent){
                            dispatchEvent(eventSingle,dispatchedEvent);
                        });
                
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
                $this.children('.prettyCalendar-wood, .wood-bottom').animate({width : '+=300px' }, 200, function() {
                    //$this.find('.add-event').show().find('.events-list').html(eventSingle.clone())
                    $this.find('.add-new input').select();
                    calcTotalDayAgain();
                    calcScroll();
                    $close.show();
                });
            });
            
            dropdown[0].click(function(){
                dropdown[2].children('.dropdown').hide(0);
                $(this).next('.dropdown').show(0);
            });
            dropdown[1].click(function(){
                $(this).parent().parent().children('span').text($(this).text());
                dropdown[2].children('.dropdown').hide(0);
            });
            $('html').click(function(){
                dropdown[2].children('.dropdown').hide(0); 
            });
            $('.add-time .select span').click(function(event){
                event.stopPropagation(); 
            });
            
            $this.on('click', allDay[0], function(){
                $(this).removeAttr('data-type').attr('data-type', 'enabled').children('.check').children().css('background-color', settings.color);
                dropdown[2].children('.dropdown').hide(0);
                $(this).parents('.all-day').prev('.add-time').css('opacity', '0.4').children('.disabled').css('z-index', '10');
            });
            $this.on('click', allDay[1], function(){
                $(this).removeAttr('data-type').attr('data-type', 'disabled').children('.check').children().css('background-color', 'transparent');
                $(this).parents('.all-day').prev('.add-time').css('opacity', '1').children('.disabled').css('z-index', '-1');
            });

            var dataId = parseInt($this.find('.total-bar b').text());
            $this.find('.submit').on('click', function(){
                var title = $(this).prev('input').val();
                var hour = $(this).parents('.add-new').find('.hour > span').text();
                var min = $(this).parents('.add-new').find('.min > span').text();
                var isAllDay = $(this).parents('.add-new').find('.all-day fieldset').attr('data-type');
                var isAllDayText = $(this).parents('.add-new').find('.all-day fieldset label').text();
                var thisDay = $this.find('.day.this-month.selected').attr('data-date');
                var time;
                if ( isAllDay == 'disabled' ) {
                    time = hour + ':' + min;
                } else {
                    time = isAllDayText;
                }
                $this.prepend(div('div', 'added-event').attr({'data-date':thisDay, 'data-time': time, 'data-title': title, 'data-id': dataId}));
                
                $this.find('.day.this-month.selected').prepend(
                    div('div','event-single').attr('data-id', dataId).append(
                        div('p','').text(title),
                        div('div', 'volunteer').append(
                            div('div', 'volunteerText').text('Volunteer?'),
                            div('div', 'volunteerIcon')
                        ),
                        div('div','details').append(
                            div('div', 'clock').text(time),
                            div('div', 'erase')
                        )
                    )
                );
                $this.find('.day').has('.event-single').addClass('have-event').prepend(div('i',''));
                $this.find('.events-list').html($this.find('.day.this-month.selected .event-single').clone())
                $this.find('.events-list .event-single').eq(0).hide().slideDown();
                calcTotalDayAgain();
                calcScroll();
                $this.find('.events-list').scrollTop(0);
                $this.find('.add-new > input[type="text"]').val(AddEvent).select();
                dataId++;
            });
            
            $close.on('click', function(){
                prevAddEvent(); 
            });
            
            $this.on('click', '.event-single .erase', function(){
                $('div[data-id=' + $(this).parents(".event-single").attr("data-id") + ']').animate({'height': 0}, function(){ 
                    $(this).remove();
                    calcTotalDayAgain();
                    calcScroll();
                });
            });

        };

    }(jQuery));

});


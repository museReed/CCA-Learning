# Survey

> Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/297276

**
  
  
    
      

# Course Satisfaction Survey - Advanced MCP


    
  
  
    
      
      

Mind sharing your thoughts and experiences around this course?


      
    
  
  
    3 questions
  
  
    
      Start
    
  


    var question_start_time;
    var question_finish_time;
    var count;
    var quiz_response_id;
    var question_id;
    var button_clicked = false;

    // Should ONLY be set in startQuiz().
    var initialQuizLoad;
    var startQuizTime;

    // Null on initial load, then initialized in quiz_question.html
    var endQuizTimeInMs;
    var countdownIntervalId;

    const wrapperSelector = "div.quiz[data-quiz=2gmk8gvgqcxeo]";

    function disableButtons() {
        button_clicked = true;
        $(wrapperSelector + " button").attr('disabled', true);
    }

    function enableButtons() {
        button_clicked = false;
        $(wrapperSelector + " button").attr('disabled', false);
    }

    function showQuiz(data) {
        if (data.success) {
            // 
            // 
            if (data.force_refresh) {
                location.reload();
            }

            $('.quiz').html(data.quiz_html);

            

            count = data.count;
            quiz_response_id = data.quiz_response_id;
            question_id = data.question_id;
            question_start_time = new Date();
            
                if (data.unlock_next_lesson) {
                    unlockNextLesson(data);
                }
            

            Prism.highlightAll();
        } else {
            console.error(data.error_msg);
        }
        enableButtons();
    }

    function getRequestData(submit) {
        var requestData = {
            'lesson_id': '3am15tyn3ohyz',
        
            'published_course_id': '1ofs8qdfctxqp',
        
            'quiz_response_id': quiz_response_id,
            'question_id': question_id
        };
        
            requestData['quiz_id'] = '2gmk8gvgqcxeo';
        
        if (submit) {
            
            var answer = $('input[name="answer"]:checked');
            if (answer.length > 0) {
                requestData['answer'] = $(answer[0]).val();
            }
            var chosen_answers = $('input[name="chosen_answers"]:checked');
            if (chosen_answers.length > 0) {
                requestData['chosen_answers'] = [];
                chosen_answers.each( function(i, li) {
                    requestData['chosen_answers'].push($(li).val());
                });
            }
            var response_text = $('input[name="response_text"], textarea[name="response_text"]');
            if (response_text.length > 0) {
                requestData['response_text'] = $(response_text[0]).val();
            }

            const linearScaleChoiceRadioSelector = 'input[name="linear-scale-question"]'
            const selectedLinearScaleAnswer = document.querySelector(`${linearScaleChoiceRadioSelector}:checked`);
            if (selectedLinearScaleAnswer) {
              requestData['answer'] = selectedLinearScaleAnswer.value;
            }

            const $uploadedContentInput = document.querySelector('#id_uploaded_content');
            if ($uploadedContentInput) {
              requestData['uploaded_content'] = $uploadedContentInput.value;
            }

            requestData['question_number'] = count;
            requestData['start_time'] = question_start_time ? question_start_time.toISOString() : null;
            requestData['finish_time'] = question_finish_time ? question_finish_time.toISOString() : null;
        }
        else {
            
            requestData['question_number'] = count - 2;
        }
        return requestData;
    }

    function startQuiz(goToStart, initialLoad) {
        var requestData = {
            'lesson_id': '3am15tyn3ohyz',
            
                'published_course_id': '1ofs8qdfctxqp',
            
        };

        
            requestData['quiz_id'] = '2gmk8gvgqcxeo';
        

        if (initialLoad) {
            requestData['load'] = true
        }

        else if (goToStart) {
            requestData['go_to_start'] = true
        }
        else {
            endQuizTimeInMs = undefined;
            initialQuizLoad = true;
            startQuizTime = new Date();
            requestData['start_time'] = startQuizTime.toISOString();
        }

        
            var url = '/quiz/start_quiz';
        

        $.post(url, requestData)
            .done(function (data) {
                showQuiz(data);
            })
            .fail(function() {
                enableButtons();
            });
    }

    function answerQuestion() {
        if (!button_clicked) {
            disableButtons();
            question_finish_time = new Date();
            var requestData = getRequestData(true);
            
                var url = '/quiz/next_question';
            

            $.ajax({
                url: url,
                type: 'POST',
                data: requestData,
                dataType: 'json',
                traditional: true
            })
            .done(function (data) {
                showQuiz(data);
                
                    courseCompletionCallback(data);
                
            })
            .fail(function () {
                enableButtons();
            });
        }
    }

    function padWithZero(num) {
        return (num >= 0 && num < 10) ? "0" + num : num + "";
    }

    function setupQuizClickHandlers() {
        $(wrapperSelector).on('click', '.create_quiz', function () {
            if (!button_clicked) {
                disableButtons();
                startQuiz(false, false);
            }
        });

        $(wrapperSelector).on('click', '.redirect_to_start_page', function() {
            if (!button_clicked) {
                disableButtons();
                startQuiz(true, false);
            }
        });

        $(wrapperSelector).on('click', '#answer_question', answerQuestion);

        $(wrapperSelector).on('click', '#prev_question', function () {
            if (!button_clicked) {
                disableButtons();
                var requestData = getRequestData(false);

                
                    var url = '/quiz/prev_question';
                

                $.post(url, requestData)
                    .done(function (data) {
                        showQuiz(data);
                    })
                    .fail(function () {
                        enableButtons();
                    });
            }

        });

        $(wrapperSelector).on('click', '.show_answers_toggle, .hide_answers_toggle', function () {
            $('.question-responses').slideToggle('fast');
            $('.hide_answers_toggle').toggle();
            $('.show_answers_toggle').toggle();
        });

        $(wrapperSelector).on('keyup', 'input[type=text]', function(e) {
            if (e.keyCode == 13) {
                $(this).blur();
                answerQuestion();
            }
        });
    }

    $(document).ready(function () {
        setupQuizClickHandlers();
        startQuiz(false, true);
    });
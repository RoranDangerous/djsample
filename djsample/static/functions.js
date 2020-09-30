let questions_count = 0;

const onCreateQuiz = e => {
  e.preventDefault();

  console.log($('form#create-quiz input[name="csrfmiddlewaretoken"]').val())
  let data = new FormData();
  data.append('csrfmiddlewaretoken', $('form#create-quiz input[name="csrfmiddlewaretoken"]').attr('value'))
  data.append('questions', JSON.stringify(getQuestions()));

  const conf = {
    method: "POST",
    body: data,
    credentials: 'same-origin'
  }

  fetch('/quiz/create/', conf)
  .then(res => {
    if(res.status === 200){
      document.location.href="/";
    } else {
      throw 'Error!'
    }
  })
  .catch(err => console.error('Error creating a quiz: ', err))
}

const getQuestions = () => {
  let result = [];

  $("form#create-quiz ol li").each((i ,v) => {
    let multiple_choice = $(v).find('input[name="type"]').is(":checked")
    let question = {
      'question': $(v).find('input[name="question"]').val(),
      'multiple_choice': multiple_choice,
      'answer': multiple_choice ? getMCAnswers(v): getSQAnswer(v)
    };

    result.push(question)
  });
  console.log(result)

  return result;
}

const getMCAnswers = el => {
  return $(el).find('.form-check').map((_, v) => ({
    'option': $(v).find('.form-check-label input').val(),
    'is_correct': $(v).find('.form-check-input').is(':checked')
  })).toArray().filter(v => v.option)
}

const getSQAnswer = el => {
  return $(el).find('input[name="answer"]').val()
}

const addNewQuestion = e => {
  e.preventDefault();

  $("form#create-quiz ol").append(Question(questions_count));

  $('form#create-quiz button[type="submit"]').removeAttr('disabled');

  questions_count++;
}

const Question = id => `
  <li>
    <div class="form-group">
      <label for="name-${id}" style="font-weight: bold;">Question:</label>
      <div class="custom-control custom-switch" style="float: right">
        <input type="checkbox" class="custom-control-input" id="mc-${id}" name="type" onchange="handleQuestionTypeChange(this, ${id})">
        <label class="custom-control-label" for="mc-${id}">Multiple Choice</label>
      </div>
      <input type="text" class="form-control" id="name-${id}" name="question" placeholder="What is the capital of Great Britain?">
    </div>
    <div class="form-group">
      <label style="font-weight: bold;">Answer:</label>
      <div id="answer-${id}">
        ${TextInput(id)}
      </div>
    </div>
  </li>
`

const handleQuestionTypeChange = (e, question_id) => {
  $(`#answer-${question_id}`).empty();

  if(e.checked){
    $(`#answer-${question_id}`).append(MultipleChoiceOption(question_id, 1));
  } else {
    $(`#answer-${question_id}`).append(TextInput());
  }
}

const TextInput = () => `<input type="text" class="form-control" name="answer" placeholder="London">`

const handleMultipleChoiceChange = (e, question_id, mc_id) => {
  let count = +e.getAttribute('count');

  if(e.value && count === mc_id){
    e.setAttribute('count', count+1);
    $(`#answer-${question_id}`).append(MultipleChoiceOption(question_id, count+1));
  }
}

const cities = ["Barcelona", "London", "Vancouver", "Kiev", "Paris"];
const MultipleChoiceOption = (question_id, mc_id) => `
  <div class="form-check mb-1">
    <input type="checkbox" class="form-check-input" style="margin-top: .75rem">
    <label class="form-check-label">
      <input type="text" class="form-control" count="${mc_id}" onkeyup="handleMultipleChoiceChange(this, ${question_id}, ${mc_id})" placeholder="${cities[(mc_id - 1) % cities.length]}">
    </label>
  </div>
`
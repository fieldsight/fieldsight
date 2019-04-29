var editing_list =[];

function safelyParseJSON (json) {
    var parsed
    try {
        parsed = JSON.parse(json);
    } catch (e) {
        parsed = [];
        // alert("Json  Error Occured Could not read Json objects." +e);
    }
    return parsed 
}

function getanswer(question){
    if(_json_answer.hasOwnProperty(question)){
        return _json_answer[question];
    }
    else{
        return "";
    }
}

_json_question.map(function(item){
    item['answer']=getanswer(item.question_name);
})

var Question = React.createClass({
    save: function () {
        this.props.updateAnswerText(this.refs.answer.value, this.props.index);
    },

    renderForm:function(){
        return(
            <div className="form-group col-md-6 QuestionContainer ">
                <label className="col-form-label" ref="newText">{this.props.question}</label>

                {this.props.question_type === 'Project' && (
                    <select className="form-control" ref="answer" onChange={this.save} defaultValue={this.props.answer}>
                        <option value="">Select a site to reference</option>
                        {this.props.project && project_sites[this.props.project] && (
                            project_sites[this.props.project].map(site => (
                                <option value={site.id} key={site.id}>{site.name}</option>
                            ))
                        )}
                    </select>
                )}

                {this.props.question_type !== 'Project' && (
                    <input className="form-control" type="text" ref="answer" onChange={this.save} defaultValue={this.props.answer}></input>      
                )}
            </div>
        );
    },
    render: function () {
        return this.renderForm();
    }
});


var MCQQuestion = React.createClass({

    getInitialState: function() {
        return {
            selectValue: this.props.answer || "Select Me"
        }
    },

    _onChange: function(event, item) {
        this.setState({
            selectValue: this.props.options[event.target.selectedIndex].label
        });
        // this.props.onChange(event.target.value);
        this.props.updateAnswerText(this.refs.answer.value, this.props.index);
    },



    render: function() {
        var selectValue = this.state.selectValue;
        var options = this.props.options.map(function(item) {
            if (selectValue === item.option_text) {
                return <option selected value = {
                    item.option_text
                } > {
                    item.option_text
                } </option>;
            } else {
                return <option value = {
                    item.option_text
                } > {
                    item.option_text
                } </option>;
            }

        })

        return ( 
            <div className="form-group col-md-6 QuestionContainer ">
                <label className="col-form-label" ref="newText">{this.props.question}</label>
                <select className="form-control" ref="answer" name={this.props.name || ''} id={this.props.id || (this.props.name || '')} onChange = {this._onChange}> 
                    {options} 
                </select>       
            </div>
        );
    }
});


var Form = React.createClass({
    getInitialState: function () {
        return {
            Questions: _json_question
        }
    },

    updateAnswer: function (answer, i) {
        // console.log('Updating Question');
        var arr = this.state.Questions;
        if (arr[i].question_type == "Number"){
            if(isNaN(answer)){
                alert("Please enter only numerical value for "+arr[i].question_text);
                arr[i].answer="";
                this.setState({Questions:arr});
                return;
            }
        }
        arr[i].answer=answer;
        this.setState({Questions:arr});
    },

    save: function () {
        var answers ={}
        var Questions = this.state.Questions
        for (var key in Questions) {
            answers[Questions[key].question_name] = Questions[key].answer;
        }
        var answer = JSON.stringify(answers);
        document.getElementById('id_site_meta_attributes_ans').value = answer;
        document.getElementById('SiteForm').submit();
    },
    eachQuestion: function (item, i){
        if(item.question_type == "MCQ"){
            return(
                <MCQQuestion key={i} index={i} options={item.mcq_options} answer={item.answer} question={item.question_text} question_type={item.question_type} updateAnswerText={this.updateAnswer} />
            );
        }
        else{
            return(
                <Question
                    key={i}
                    index={i}
                    answer={item.answer}
                    question={item.question_text}
                    question_type={item.question_type}
                    updateAnswerText={this.updateAnswer}
                    project={item.project}
                    project_field={item.project_field}
                />
            );
        }
    },
    render: function () {
        return (
            <div>
                <div className="Form form-row">
                    {   
                        this.state.Questions.map(this.eachQuestion)
                    }
                </div>
                <button className="btn btn-success" onClick={this.save.bind()} >Save Form</button>
            </div>
        );
    }
});


ReactDOM.render(<Form /> , document.getElementById('metaattribs')
);


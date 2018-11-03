import React, { Component } from 'react';
import { API_URL, DEFAULT_USER_PIC} from "../abstract/variables";
import moment from "moment";
import Button from './UI/button';
import ErrorPopup from './UI/errorPopup';
import axios from 'axios';
import MultiLineTextInput from './UI/MultiLineTextInput';
import TextInput from './UI/textInput';
import IconButton from './UI/iconButton';

class CommentingSystem extends Component {
    constructor(props){
            super(props);

            this.setCommentInput = this.setCommentInput.bind(this);
            this.reloadAjaxRequest = this.reloadAjaxRequest.bind(this);
            this.setComments = this.setComments.bind(this);
            this.getComments = this.getComments.bind(this);
            this.toggleViewAll = this.toggleViewAll.bind(this);
            this.clearComments = this.clearComments.bind(this);

            this.state = {
                errorPopup:{},
                preview:this.props.preview == undefined ? {state:false,count:0} : this.props.preview,
                userId:"",
                comments:{
                    data: []
                },
                ajax: {
                    getComments: {
                        attempts: 0,
                        error: ""
                    }
                }
            }
        }

    componentDidMount(){
        var state = this.props.parent.state;
        state.commentingSystem = this;
        this.props.parent.setState(state);

        this.getComments();
    }

    clearComments(){
        var state = this.state;

        if (state.comments.data.length > 0 ){
            state.comments = {
                data: []
            }

            this.setState(state);
            console.log("Comments Cleared!");
        }
    }

    setCommentInput(){
        return <CommentInput main={this} />
    }

    setComments() {
        var comments = this.state.comments.data;
        var preview = this.state.preview;

        if (comments != [] || comments != null) {
            comments = comments.reverse();
            console.log(comments);

            return (
                comments.map((item,i)=>{
                    if(preview.state == true && preview.count <= i){   return;  }
                    else{
                        return <Comment key={i} comment={item} main={this} />;
                    }
                })
            );
        }
        else {
            return <NoCommentPlaceholder />;
        }
    }

    reloadAjaxRequest(option) {
        var state = this.state;

        switch (option) {
            case 1: {

                if (state.ajax.getComments.attempts < 5) {
                    state.ajax.getComments.attempts += 1;
                    this.setState(state);
                    this.getComments();
                }
                else {
                    state.errorPopup.displayError("Access to server failed. Try again Later! ");
                    state.ajax.getComments.attempts = 0;
                    this.setState(state);
                }
                break;
            }
        }

    }

    getComments() {
        var component = this;
        var state = this.state;
        var url = API_URL;

        switch(this.props.commentingOn){
            case 1:{
                url += "comment/" + this.props.product.post.id;
                break;
            }
        }

        url += state.comments.data.length == 0 || state.comments.data == undefined ? "/1/0" : "/1/" + state.comments.data.length;

        axios({
            url:url,
            method:"GET"
        }).then((response)=>{

            switch(response.status){
                case 200:{
                    if (data.content != []) {
                        state.comments.data = data.content.concat(state.comments.data);
                        state.userId = data.userId;
                        component.setState(state);
                    }
                    break;
                }
            }
            
        }).catch(() =>{
            component.reloadAjaxRequest(1);
        })

    }

    toggleViewAll(){
        var state = this.state;
        state.preview.state = state.preview.state == false ? true :false;
        this.setState(state);
    }

    setToggleViewAll(){
        var state = this.state;

        if(state.preview.count > 0 && state.comments.data.length > state.preview.count){
            var text = state.preview.state ? "View more ..." : "Collapse";
            return (<div className="commentSection__vMore f_normal" onClick={() => { this.toggleViewAll() }}>{text}</div>);
        }
        else {
            return (<div></div>);
        }
        
    }

    render() {
        return (
            <div className="commentSection">
                <ErrorPopup parent={this}/>
                <div className="commentSection__title f_h1">{this.state.comments.data.length + ' comments'}</div>
                {this.setCommentInput()}
                {this.setComments()}
                {this.setToggleViewAll()}
            </div>
        );
    }
}


class CommentInput extends Component {
    constructor(props){
        super(props);

        this.postComment = this.postComment.bind(this);
        this.reloadAjaxRequest = this.reloadAjaxRequest.bind(this);

        this.state = {
            textInputs:[],
            buttons:[],
            ajax:{
                postComment:{
                    attempts:0
                }
            }
        }
    }

    reloadAjaxRequest(option) {
        var state = this.state;

        switch (option) {
            case 1: {

                if (state.ajax.postComment.attempts < 10) {
                    state.ajax.postComment.attempts += 1;
                    this.setState(state);
                    this.postComment();
                }
                else {
                    this.props.parent.state.errorPopup.displayError("Access to server failed. Try again Later! ");
                    state.ajax.postComment.attempts = 0;
                    this.setState(state);
                }
                break;
            }
        }

    }

    postComment(){
        var component = this;
        var state = this.state;
        var textInputs = state.textInputs;

        textInputs.forEach((elem,i)=>{

            if(elem.state.inputValue == ""){
                elem.state.status = 1;
                elem.focus();
                return; 
            }
        })

        var formData = {
            name:textInputs[0].state.inputValue,
            email: textInputs[1].state.inputValue,
            comment: textInputs[2].state.inputValue
        }

        var url = API_URL + "comment/" + this.props.main.props.commentingOn + "/";

        switch(this.props.main.props.commentingOn){
            case 1:{
                url += this.props.main.props.product.log.id + "/0";
                break;
            }
        }

        state.buttons[0].setStatus(3);
        var errorPopup = this.props.main.state.errorPopup;

        axios({
            url:url,
            method:"POST",
            data:formData
        }).then((response)=>{

            switch (response.status) {
                case 201: {
                    state.buttons[0].setStatus(2);
                    component.props.main.getComments();
                    break;
                }
            }

        }).catch((response)=>{
            state.buttons[0].setStatus(1);

            switch(response.status){
                case 400:
                case 500:{
                    errorPopup.displayError("Access to server failed. Try again Later! ");
                    break;
                }
                case 404:{
                    errorPopup.displayError("Post not found. Try again Later! ");
                    break;
                }
            }

        });

    }

    render() {
        var c = this;

        return (
            <div className="commentInput">
                <div className="commentInput__form">
                    <div className="commentInput__user">
                        <div className="commentInput__user__pic">
                            <img src={DEFAULT_USER_PIC[1]} />
                        </div>
                    </div>

                    <div className="commentInput__user__details">
                        <div className="commentInput__user__name">
                            <TextInput
                                parent={this}
                                status={0}
                                config={{
                                    label: "",
                                    length:60,
                                    type: "text_input_4",
                                    placeholder:"Name ...",
                                    comment: "Maximum characters allowed is (60)."
                                }} />
                        </div>

                        <div className="commentInput__user__email">
                            <TextInput
                                parent={this}
                                status={0}
                                config={{
                                    label: "",
                                    type: "text_input_4",
                                    placeholder: "Email Address ...",
                                    comment: "Maximum characters allowed is (80)."
                                }} />
                        </div>
                    </div>

                    <div className="commentInput__box">
                        <MultiLineTextInput 
                            parent={this}
                            status={0}
                            config={{
                                label:"Comment",
                                type:"mul_text_input",
                                placeholder: "Add a comment..."
                            }}
                        />


                        <div className="commentInput__sendBtn">
                            <Button 
                                parent={this} 
                                config={{ 
                                    type: "btn_1", 
                                    action: this.postComment, 
                                    label: "Send", 
                                    text: "" }} 
                                status={0} />
                        </div>
                    </div>

     
                </div>
            </div>
        );
    }
}


class NoCommentPlaceholder extends Component {
    render() {
        return (
            <div className="noComment">
                <div className="noComment__text f_normal">No one has commented on this post yet. Be the first. </div>
            </div>
        );
    }
}

class Comment extends Component {
    constructor(props){
        super(props);
        var stats = {
            likes:0,
            dislikes:0
        }

        this.props.comment.stats.forEach((s)=>{
            switch(s.reaction){
                case 1:{
                    stats.likes ++;
                    break;
                }
                case 2:{
                    stats.dislikes ++;
                    break;
                }
            }
        })

        this.state = {
            reaction:0,
            stats: stats,
            iconButtons:[]
        }

        this.checkIfLiked = this.checkIfLiked.bind(this);
        this.reactToComment = this.reactToComment.bind(this);
    }

    componentDidMount(){
        this.checkIfLiked();
    }

    reactToComment(reaction = 1){
        var component = this;
        var state = component.state;

        //Reactions
        //1 - Like
        //2 - Dislike

        var url = API_URL + "commentReaction/" +  this.props.main.props.commentingOn +"/"+ this.props.comment.id + "/";
        url += state.reaction == reaction ? 0 : reaction;

        axios({
            url:url,
            method:"GET"
        }).then((response)=>{
            
            switch(response.status){
                case 200: {
                    var prevReaction = state.reaction;
                    state.reaction = reaction;
                    console.log("Reaction change : " + prevReaction + " " + reaction);

                    switch (prevReaction){
                        case 0:{
                            switch (reaction) {
                                case 1: {
                                    state.stats.likes++;
                                    break;
                                }
                                case 2: {
                                    state.stats.dislikes++;
                                    break;
                                }
                            }
                            break;
                        }
                        case 1:{
                            switch (reaction) {
                                case 2: {
                                    state.stats.likes--;
                                    state.stats.dislikes++;
                                    break;
                                }
                            }
                            break;
                        }
                        case 2:{
                            switch (reaction) {
                                case 1: {
                                    state.stats.dislikes--;
                                    state.stats.likes++;
                                    break;
                                }
                            }
                            break;
                        }
                    }

                    component.setState(state);
                    component.checkIfLiked();
                    break;
                }
            }

        }).catch((response) => {
            switch(response.status){
                case 404:{
                    component.props.main.state.errorPopup.displayError("Comment not found! Try again later!");
                    break;
                }
            }
        })
    }

    checkIfLiked(){
        var comment = this.props.comment;
        var state = this.state;
        var userId = this.props.main.state.userId;

        var reaction = comment.stats.find((item)=>{
            return item.user == userId;
        })

        state.reaction = reaction == undefined ? 0 : reaction.reaction;


        state.iconButtons[0].state.status = state.reaction == 2 ? 5 : 0;
        state.iconButtons[1].state.status = state.reaction == 1 ? 6 : 0;

        this.setState(state);
    }


    render() {
        var comment = this.props.comment;
        var time = moment(comment.created_at, "YYYY-MM-DDTHH:mm:ss").utc(3).local();
        var reaction = this.state.reaction;

        return (
            <div className="comment" >
                <div className="comment__user">
                    <div className="comment__user__pic">
                        <img src={DEFAULT_USER_PIC[1]} />
                    </div>
                </div>

                <div className="comment__right">
                    <div className="comment__right__top">
                        <div className="comment__right__top__name f_h2">{comment.userName}</div>
                        <div className="comment__right__top__time f_normal">{moment.duration(moment().diff(time)).humanize() + " ago"}</div>
                    </div>

                    <div className="comment__text f_normal">{comment.comment}</div>

                    <div className="comment__bottom">
                        <div className="comment__stats">

                            <div className="comment__stats__likes">
                                <div className="comment__stats__icon">
                                    <IconButton 
                                        parent={this}
                                        status={reaction == 2 ? 5 : 0}
                                        config={{
                                            icon: "dislike",
                                            class: "iconBtn",
                                            action: () => { this.reactToComment(2)}
                                        }}
                                    />
                                </div>
                                <div className="comment__stats__values f_normal">{this.state.stats.dislikes}</div>
                            </div>


                            <div className="comment__stats__likes">
                                <div className="comment__stats__icon">
                                    <IconButton
                                        parent={this}
                                        status={reaction == 1 ? 6 : 0}
                                        config={{
                                            icon: "like",
                                            class: "iconBtn",
                                            action: () => { this.reactToComment(1)}
                                        }}
                                    />
                                </div>
                                <div className="comment__stats__values f_normal">{this.state.stats.likes}</div>
                            </div>

                            
                        </div>
                    </div>

                </div>
            </div>
        );
    }
}

export default CommentingSystem;

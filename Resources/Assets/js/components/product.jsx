import React, { Component } from 'react';
import webUrl from '../abstract/variables';
import moment from 'moment';

class Article extends Component {
    constructor(props) {
        super(props);

        this.returnArticle = this.returnArticle.bind(this);
    }

    returnArticle(){
        switch(this.props.type){
            case 1:{    return <Article_1 post={this.props.post}/>;    }
            case 2:{    return <Article_2 post={this.props.post}/>}
        }
    }

    render() {
        return (
            this.returnArticle()
        );
    }
}

class Article_1 extends Component {
    render() {
        var post = this.props.post;
        const image = {
            backgroundImage: 'url("' + webUrl + "accounts/institution/" + post.log.owner_id + "/" + post.image.name + "." + post.image.type + '")'
        }

        return (
            <div className="art--1__con" id={"p-" + post.log.id}>

                <div className="art--1__con__up" style={image}>
                    <a href={webUrl + "article/" + post.log.owner_id + "/" + post.log.id}>
                        <div className="art--1__link">
                            <div className="art--1__title f_normal f_text-capitalize">{post.post.title}</div>
                            <svg className="icon">
                                <use xlinkHref="#view" />
                            </svg>
                        </div>
                    </a>
                </div>

                <div className="art--1__con__down">

                    <div className="art--1__stat">
                        <div className="art--1__stat__view">
                            <div className="art--1__stat__icon">
                                <div className="btn_icon--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#view" />
                                    </svg>
                                </div>
                            </div>
                            <div className="art--1__stat__value f_h2 f_text-bold">{post.post.stat.views}</div>
                        </div>

                        <div className="art--1__stat__likes">
                            <div className="art--1__stat__icon">
                                <div className="btn_icon--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#like" />
                                    </svg>
                                </div>
                            </div>
                            <div className="art--1__stat__value f_h2 f_text-bold">{post.post.stat.likes}</div>
                        </div>

                        <div className="art--1__stat__com">
                            <div className="art--1__stat__icon">
                                <div className="btn_icon--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#communication" />
                                    </svg>
                                </div>
                            </div>
                            <div className="art--1__stat__value f_h2 f_text-bold">{post.post.stat.comments}</div>
                        </div>

                    </div>
                </div>
            </div>
        );
    }
}

class Article_2 extends Component {
    constructor(props){
        super(props);

        this.state = {
            user:{
                name:"",
                ppic:""
            }
        }

        this.setUserDetails = this.setUserDetails.bind(this);
    }

    componentWillMount(){
        this.setUserDetails();
    }

    setUserDetails(){
        var post = this.props.post;
        var user = post.user;
        var state = this.state;

        switch (post.log.owner_type) {
            case 1: {
                state.name = user.username;

                if (user.profilePic != undefined) {
                    state.user.ppic = webUrl + 'accounts/student/' + user.id + "/" + student.profilePic.name + "/dp_50_50.png";
                }
                else {
                    state.user.ppic = webUrl + 'assets/images/student.jpg';
                }
                break;
            }
            case 2: {
                break;
            }
            case 3: {
                state.user.name = user.institution.name;
                state.user.link = webUrl + user.institution.code;

                if (user.insLogo != undefined) {
                    state.user.ppic = webUrl + 'accounts/institution/' + user.id + "/" + student.insLogo.name + "/dp_50_50.png";
                }
                else {
                    state.user.ppic = webUrl + 'assets/images/student.jpg';
                }
                break;
            }
        }

        this.setState(state);
    }

    render() {
        var post = this.props.post;
        var user = this.state.user;
        const image = {
            backgroundImage: 'url("' + webUrl + "accounts/institution/" + post.log.owner_id + "/" + post.image.name + "." + post.image.type + '")'
        }

        var ctime = moment.utc(post.log.created_at.date, 'YYYY-MM-DD HH:mm:ss.SSSS');
        
        return (
            <div className="art--2__con" id={"p-" + post.log.id}>
                <div className="userDetails">
                    <a href={user.link}>
                        <div className="userDetails__pic"><img src={user.ppic} /></div>
                        <div className="userDetails__name f_h1">{user.name}</div>
                    </a>
                    <div className="userDetails__time f_normal">{moment.duration(moment().diff(ctime)).humanize() + " ago"}</div>
                </div>
                
                <div className="art--2__con__up" style={image}>
                    <a href={webUrl + "article/" + post.log.owner_id + "/" + post.log.id}>
                        <div className="art--2__link">
                            <div className="art--2__title f_normal f_text-capitalize">{post.post.title.substr(0,59)}</div>
                            <svg className="icon">
                                <use xlinkHref="#view" />
                            </svg>
                        </div>
                        <div className="art--2__summary f_normal">{post.post.summary}</div>
                    </a>
                </div>

                <div className="art--2__con__down">

                    <div className="art--2__stat">
                        <div className="art--2__stat__view">
                            <div className="art--2__stat__icon">
                                <div className="btn_icon--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#view" />
                                    </svg>
                                </div>
                            </div>
                            <div className="art--2__stat__value f_h2 f_text-bold">{post.post.stat.views}</div>
                        </div>

                        <div className="art--2__stat__likes">
                            <div className="art--2__stat__icon">
                                <div className="btn_icon--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#like" />
                                    </svg>
                                </div>
                            </div>
                            <div className="art--2__stat__value f_h2 f_text-bold">{post.post.stat.likes}</div>
                        </div>

                        <div className="art--2__stat__com">
                            <div className="art--2__stat__icon">
                                <div className="btn_icon--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#communication" />
                                    </svg>
                                </div>
                            </div>
                            <div className="art--2__stat__value f_h2 f_text-bold">{post.post.stat.comments}</div>
                        </div>

                    </div>
                </div>
            </div>
        );
    }
}

export default Article;
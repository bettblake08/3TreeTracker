import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';
import Button from "../UI/button";
import ErrorPopup from '../UI/errorPopup';
import humanize from '@nlib/human-readable';
import Repo from '../repo';
import { webUrl, defaultProductCoverPic } from '../../abstract/variables';
import Popup from '../UI/popup';
import TagInput from '../tagInput';
import BalloonEditor from "@ckeditor/ckeditor5-build-balloon";
import CKEditor from "@ckeditor/ckeditor5-react";
import TextInput from '../UI/textInput';
import MultiLineText from '../UI/MultiLineTextInput';
import ButtonWithIcon from '../UI/buttonWithIcon';

class Products extends Component {
    constructor(props) {
        super(props);

        this.state = {
            view: 1,
            AddProduct:{},
            EditProduct:{},
            ProductsView:{}
        }

        this.setView = this.setView.bind(this);
    }

    setView(option) {
        var state = this.state;
        state.view = option;
        this.setState(state);
    }


    render() {
        var view = this.state.view;
        var viewClass = "view__options";

        switch (view) {
            case 1: {
                viewClass += "--1";
                break;
            }
            case 2: {
                viewClass += "--2";
                break;
            }
            case 3: {
                viewClass += "--3";
                break;
            }
        }

        return (

            <div id="section_1" className="SB">

                <div className={this.state.view == 1 ? "view--active" : "view--disabled"}>
                    <ProductsView parent={this}/>
                </div>

                <div className={this.state.view == 2 ? "view--active" : "view--disabled"}>
                    <AddProduct parent={this} />
                </div>

                <div className={this.state.view == 3 ? "view--active" : "view--disabled"}>
                    <EditProduct parent={this} productId={0} />
                </div>

            </div>
        );
    }
}

class ProductsView extends Component {
    constructor(props) {
        super(props);

        var Viewable = {
            product:true,
            event: true,
            notice: true
        };

        this.state = {
            viewable:Viewable,
            content:[],
            offset:0,
            buttons:[],
            errorPopup:{},
            viewType: {
                product: 1,
                event: 1,
                notice: 1
            }
        }

        this.getProducts = this.getProducts.bind(this);
    }

    componentDidMount(){
        this.getProducts();
    }

    getProducts(reset = false) {
        var c = this;
        var state = c.state;

        if(reset){
            state.offset = 0;
            state.content = [];
        }

        axios({
            url: webUrl + "admin/getProducts/" + state.offset,
            method:"GET"
        }).catch((response) => {
            
            switch(response.status){
                case 202:{
                    break;
                }
                default:{
                    setTimeout(() => {
                        c.getProducts();
                    }, 1000)
                    break
                }
            }

        }).then((response)=>{
            var data = response.data;

            switch(data.error){
                case 0:{

                    if(data.content.length == 0){
                        state.errorPopup.displayError("There are no more products to retrieve. Continue creating more.");
                        break;
                    }

                    state.content = state.content.concat(data.content) ;
                    state.offset += data.content.length;
                    c.setState(state);
                    break;
                }
            }
        })

    }

    render() {
        var c = this;
        return (
                <div id="content">
                    <ErrorPopup parent={this} />
                    <div className="topBar row">
                        <div className="topBar__title f_h1 f_text-left f_text-capitalize"></div>
                        <div className="topBar__right">

                            <div className="topBar__right__add">
                                <ButtonWithIcon
                                    parent={this}
                                    status={0}
                                    config={{
                                        class: "btnIcon_1",
                                        label: "Product",
                                        text: "",
                                        icon:"add-2",
                                        action: () => {
                                            c.props.parent.setView(2)
                                        }
                                    }} />
                            </div>

                        </div>
                    </div>

                    <div className="content__view">

                        {
                            this.state.content.map((item, i) => {
                                switch (item.log.type) {
                                    case 1: {
                                        if (!this.state.viewable.product) { return; }

                                        switch (this.state.viewType.product) {
                                            case 1: { return <Product post={item} key={i} parent={this}/>; }
                                        }

                                        break;
                                    }
                                }
                            })
                        }
                    </div>

                    <div className="loadBtn">
                        <Button
                            parent={this}
                            status={0}
                            config={{
                                type: "btn_1",
                                label: "More",
                                text: "",
                                action: () => {
                                    c.getProducts()
                                }
                            }} />
                    </div>
                </div>
        );
    }
}


class Product extends Component {
     render() {
        var post = this.props.post;
        var parent = this.props.parent.props.parent;

        const image = {
            background: 'url("' + webUrl + "repo/" + post.post.image.name + '/thumb_150_150.jpg")',
            backgroundPosition: 'center',
            backgroundSize: 'cover'
        }

        var time = moment(post.log.created_at, "YYYY-MM-DD HH:mm:ss").utc(3).local();
        var ctime = moment.duration(time.diff(moment()), 'milliseconds').humanize();
        
        return (
            <div className="pro--1__con" id={"p-" + post.log.id}>
                <div className="pro--1__con__up" style={image} 
                    onClick={
                        ()=>{
                            parent.setView(3)
                            parent.state.editProduct.state.productId = post.post.id;
                            parent.state.editProduct.getProduct();
                        }}></div>
                
                <div className="pro--1__con__down">

                    <div className="pro--1__title f_h1 f_text-capitalize">{post.post.title}</div>
                    <div className="pro--1__time f_comment_1 f_text-capitalize ">{ctime + " ago"}</div>
                    <div className="pro--1__text f_normal">{post.post.summary}</div>

                    <div className="pro--1__stat">
                        <div className="pro--1__stat__view">
                            <div className="pro--1__stat__icon">
                                <div className="iconBtn--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#view" />
                                    </svg>
                                </div>
                            </div>
                            <div className="pro--1__stat__value f_h2 f_text-bold">{humanize(post.post.stat.views)}</div>
                        </div>

                        <div className="pro--1__stat__likes">
                            <div className="pro--1__stat__icon">
                                <div className="iconBtn--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#like" />
                                    </svg>
                                </div>
                            </div>
                            <div className="pro--1__stat__value f_h2 f_text-bold">{humanize(post.post.stat.reactions)}</div>
                        </div>

                        <div className="pro--1__stat__com">
                            <div className="pro--1__stat__icon">
                                <div className="iconBtn--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#communication" />
                                    </svg>
                                </div>
                            </div>
                            <div className="pro--1__stat__value f_h2 f_text-bold">{humanize(post.post.stat.comments)}</div>
                        </div>



                        <div className="pro--1__edit"
                                onClick={
                                ()=>{
                                    parent.setView(3)
                                    parent.state.editProduct.state.productId = post.post.id;
                                    parent.state.editProduct.getProduct();
                                }}>
                            <div className="iconBtn--success">
                                <svg className="icon">
                                    <use xlinkHref="#edit" />
                                </svg>
                            </div>
                        </div>
                    

                    </div>
                </div>
            </div>
        );
    }
}

class AddProduct extends Component {
    constructor(props) {
        super(props);

        this.product_submit = this.product_submit.bind(this);
        this.handleSummaryChange = this.handleSummaryChange.bind(this);
        this.handleTitleChange = this.handleTitleChange.bind(this);
        this.loadRepo = this.loadRepo.bind(this);
        this.toggleRepo = this.toggleRepo.bind(this);
        this.onProductBodyChange = this.onProductBodyChange.bind(this);

        this.state = {
            toggleRepo: false,
            loaded: false,
            popups: [],
            errorPopup: {},
            tags: [],
            textInputs: [],
            buttons: [],
            editor: {},
            form: {
                title: {
                    value: "",
                    error: ""
                },
                body: "<p>Start editing now!</p>",
                summary: {
                    value: "",
                    error: ""
                }
            }
        }

    }

    componentDidMount() {
        var c = this;
        var state = this.state;
        state.loaded = true;
        this.setState(state);
    }

    onProductBodyChange(event, editor) {
        var state = this.state;
        state.form.body = editor.getData().substr(0, 60000);
        this.setState(state);
    }

    product_submit() {
        var imageFile = document.querySelector('#img_select__img').dataset.image;       //Check if image has been selected

        if (imageFile == undefined || imageFile.length == 0) {
            this.toggleRepo();
            return;
        }
        else {
            imageFile = JSON.parse(imageFile);
        }

        var textInputs = this.state.textInputs;

        textInputs.forEach((elem) => {
            if (elem.state.inputValue == "") {
                elem.focus();
            }
        })

        if (form.body == "") {
            document.querySelector("#pro__text").focus();
            return;
        }

        var tags = [];

        this.state.tags.forEach((elem) => {
            tags.push(elem.id)
        });

        var formData = {
            pro__image: imageFile.id,
            pro__title: form.title.value,
            pro__body: form.body,
            pro__summary: form.summary.value,
            pro__tags: tags
        };

        var errorPopup = this.state.errorPopup;

        axios({
            url: webUrl + "admin/product/0",
            method: "POST",
            data: formData
        }).then((response) => {
            var data = response.data;

            switch (data.error) {
                case 0: {
                    window.location.href = webUrl + "admin/products";
                    break;
                }
                case 1: {
                    errorPopup.displayError("Failed to save the product. Please try again");
                    break;
                }
            }
        }).catch(() => {
            errorPopup.displayError("Failed to access server. Please try again in a few minutes.");
        })

    }

    handleTitleChange(e) {
        var state = this.state;
        state.form.title.value = e.target.value.substr(0, 79);
        this.setState(state);
    }

    handleSummaryChange(e) {
        var state = this.state;
        state.form.summary.value = e.target.value.substr(0, 199);
        this.setState(state);
    }

    toggleRepo() {
        this.state.popups[0].toggleContent();
    }

    loadRepo() {
        if (this.state.loaded == true) {
            return (<Popup component={<Repo parent={this} sType={1} rCount={1} token={this.props.token} userType={3} />} parent={this} />);
        }
    }

    render() {
        var c = this;
        var placeholder = {
            backgroundImage: "url('" + defaultProductCoverPic + "')",
            backgroundPosition: 'center',
            backgroundSize: 'cover'
        }

        BalloonEditor.defaultConfig.toolbar.items = [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            'bulletedList',
            'numberedList',
            'imageUpload',
            'blockQuote',
            'undo',
            'redo'
        ];

        return (
            <div className="view--scrollable SB">
                <div id="content--full">
                    <ErrorPopup parent={this} />

                    <div className="base">
                        <form method="post" encType="multipart/form-data" style={{ margin: 0, padding: 0 }}>
                            {/* <!-- IMAGE SELECT AREA--> */}

                            <div id="pro__image">
                                <div id="img_select">
                                    <div id="img_select__img" className="repoImagePreview" style={placeholder}>
                                        <input type="hidden" id="art_selected_image" name="image" />
                                    </div>
                                    <div id="img_select__buttons">
                                        <div className="btnIcon_1" onClick={() => { this.toggleRepo() }}>
                                            <div className="btnIcon_1__icon">
                                                <svg className="icon">
                                                    <use xlinkHref="#repo" />
                                                </svg>
                                            </div>
                                            <div className="btnIcon_1__label f_button_2 f_text-capitalize">Repo</div>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            {/* <!-- IMAGE SELECT AREA--> */}

                            <div id="pro__form" >
                                {/* <!-- ARTICLE TITLE AREA--> */}
                                <div id="pro__title">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            label: "Title",
                                            type: "text_input_4",
                                            comment: "Maximum characters allowed is (80). Currently, its ( " + this.state.form.title.value.length + " )"
                                        }} />
                                </div>
                                {/* <!-- ARTICLE TITLE AREA--> */}

                                {/* <!-- ARTICLE TEXT AREA--> */}
                                <div id="pro__textBox">
                                    <div id="pro__textBox__label" className="f_h1 f_text-capitalize">Body Text</div>
                                    <div id="pro__textBox__input ck--1">
                                        <CKEditor
                                            editor={BalloonEditor}
                                            data={this.state.form.body}
                                            onChange={this.onProductBodyChange}
                                        />
                                    </div>

                                    <div className="comment f_comment_1 f_text-capitalize">Maximum characters allowed is (60000). Currently, its ( {this.state.form.body.length} ) </div>

                                </div>
                                {/* <!-- ARTICLE TEXT AREA--> */}

                                {/* <!-- ARTICLE SUMMARY AREA--> */}
                                <div id="pro__summaryBox">
                                    <MultiLineText
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            label: "Summary",
                                            type: "mul_text_input",
                                            comment: "Maximum characters allowed is (200). Currently, its ( " + this.state.form.summary.value.length + " )"
                                        }} />

                                </div>
                                {/* <!-- ARTICLE SUMMARY AREA--> */}


                                <div id="pro__summaryBox">
                                    <div id="pro__summaryBox__label" className="f_h1 f_text-capitalize">Tags</div>
                                    <div id="pro__summaryBox__input" >
                                        <TagInput main={this} parent={this} />
                                    </div>
                                </div>

                                <div id="pro__save">
                                    <Button parent={this} status={0} config={{
                                        label: "Save",
                                        action: this.product_submit,
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>

                                <div id="pro__return">
                                    <Button parent={this} status={0} config={{
                                        label: "Back",
                                        action: ()=>{
                                            c.props.parent.setView(1)
                                        },
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>

                            </div>
                        </form>
                    </div>


                    {this.loadRepo()}
                </div>

            </div>
              );
    }
}

class EditProduct extends Component {
    constructor(props){
        super(props);

        this.reloadAjaxRequest = this.reloadAjaxRequest.bind(this);
        this.getProduct = this.getProduct.bind(this);
        this.setCoverImage = this.setCoverImage.bind(this);

        this.state = {
            ajax:{
                getProduct: {
                    error: "",
                    attempts: 0
                },
                getExtraData:{
                    error:"",
                    attempts:0
                }
            },
            productId: 0,
            product:{
                log:{
                    id:"",
                    type:"",
                    created_at:""
                },
                post:{
                    title:"",
                    body: "",
                    summary: "",
                    id: "",
                    tags:[]
                }
            },
            updated:false,
            errorPopup:{}
        }

    }


    componentDidMount(){
       var state = this.props.parent;
       state.editProduct = this;
       this.props.parent.setState(state);
    }

    reloadAjaxRequest(option) {
        var state = this.state;

        switch (option) {
            case 1: {

                if (state.ajax.getExtraData.attempts < 10) {
                    state.ajax.getExtraData.attempts += 1;
                    this.setState(state);
                    this.getExtraData();
                }
                else {
                    state.errorPopup.displayError("Access to server failed. Try again Later! ");
                    state.ajax.getExtraData.attempts = 0;
                    this.setState(state);
                }
                break;
            }
            case 2: {

                if (state.ajax.getProduct.attempts < 10) {
                    state.ajax.getProduct.attempts += 1;
                    this.setState(state);
                    this.getProduct();
                }
                else {
                    state.errorPopup.displayError("Access to server failed. Try again Later! ");
                    state.ajax.getProduct.attempts = 0;
                    this.setState(state);
                }
                break;
            }
        }
    }
    
    getProduct() {
        var component = this;
        var state = component.state;
        var url = webUrl + "admin/product/"+ state.productId;

        axios({
            url:url,
            method:"GET"
        }).catch((response) => {
            if (response.status != 200) {
                component.reloadAjaxRequest(2);
            }
        }).then((response)=>{
            var data = response.data;

            switch (data.error) {
                case 0: {
                    state.updated = true;
                    state.product = data.content;
                    component.setState(state);
                    component.setCoverImage();
                    break;
                }
            }
        })

    }

    setCoverImage() {
        var state = this.state;

        if(state.product.post.image != undefined){
            var preview = document.querySelectorAll(".repoImagePreview");

            preview.forEach((e)=>{
                e.setAttribute('style', "background:" + "url(\"" + webUrl + 'repo/' + state.product.post.image.name + "." + state.product.post.image.type + "\") center ; background-size:cover;");
                e.dataset.image = JSON.stringify(state.product.post.image);
            })
            
        }
    }

    render() {
        if(this.state.product.post == undefined || this.state.product.post.title == undefined){   return <div></div>; }

        return (
            <div className="view--scrollable SB">
                <ErrorPopup parent={this}/>
                <div className="product"><Edit parent={this}/></div>
            </div>

        );
    }
}

class Edit extends Component {
    constructor(props){
        super(props);

        this.state = {
            toggleRepo:false,
            textInputs:[],
            buttons:[],
            data: {
                currency: [],
                duration: []
            },
            form: {
                title: {
                    value: "",
                    error: ""
                },
                summary: {
                    value: "",
                    error: ""
                },
                body: ""
            },
            updated:false,
            popups: [],
            tags:[]
        }

        this.setProductData = this.setProductData.bind(this);
        this.handleProductBodyChange = this.handleProductBodyChange.bind(this);
        this.toggleRepo = this.toggleRepo.bind(this);
        this.loadRepo = this.loadRepo.bind(this);
        this.product_submit = this.product_submit.bind(this);
    }

    componentDidMount(){
        var state = this.state;
        state.loaded = true;
        this.setState(state);
        this.setProductData();
    }

    componentDidUpdate(){
        if (this.props.parent.state.updated != this.state.updated){
            this.setProductData();
        }
    }

    setProductData() {
        var state = this.state;
        var product = this.props.parent.state.product.post;
        
        if (product != null) {

            state.textInputs[0].state.inputValue = product.title;
            state.textInputs[1].state.inputValue = product.summary;
            state.form.body = product.body;
            state.tags = product.tags;
            state.updated = this.props.parent.state.updated;
            
            this.setState(state);
        }
        else {
            this.props.parent.getProduct();
        }
    }

    handleProductBodyChange(event, editor) {
        var state = this.state;
        state.form.body = editor.getData().substr(0, 60000);
        this.setState(state);
    }

    product_submit() {
        var imageFile = document.querySelector('.repoImagePreview').dataset.image;       //Check if image has been selected

        if (imageFile == undefined || imageFile.length == 0) {
            this.toggleRepo();
            return;
        }
        else {
            imageFile = JSON.parse(imageFile);
        }

        var textInputs = this.state.textInputs;

        textInputs.forEach((elem)=>{
            if(elem.state.inputValue == ""){
                elem.focus();
            }
        })
    
        if (this.state.form.body == "") {
            document.querySelector(".form__textBox").focus();
            return;
        }

        var tags = [];

        this.state.tags.forEach((elem) => {
            tags.push(elem.id)
        });

        var formData = {
            pro__image: imageFile.id,
            pro__title: textInputs[0].state.inputValue,
            pro__body: this.state.form.body,
            pro__summary: textInputs[2].state.inputValue,
            pro__tags: JSON.stringify(tags)
        };

        var errorPopup = this.state.errorPopup;

        axios({
            url: webUrl + "admin/product/" + this.props.parent.state.product.post.id,
            method: "PUT",
            data: formData
        }).then((response) => {
            var data = response.data;

            switch (data.error) {
                case 0: {
                    window.location.href = webUrl + "admin/products";
                    break;
                }
                case 1: {
                    errorPopup.displayError("Product does not exist! If you have an concerns, contact developer!");
                    break;
                }
                case 2: {
                    errorPopup.displayError("Failed to save the product. Please try again!");
                    break;
                }
            }
        }).catch((response) => {
            if(response.status != 200){
                errorPopup.displayError("Failed to access server. Please try again in a few minutes.");
            }
        })

    }

    toggleRepo() {
        this.state.popups[0].toggleContent();
    }

    loadRepo() {
        if (this.state.loaded == true) {
            return (<Popup component={<Repo parent={this} sType={1} rCount={1} token={this.props.token} userType={3} />} parent={this} />);
        }
    }

    render() {
        var parent = this.props.parent.props.parent;

        return (
            <div id="editProduct">
                <ErrorPopup parent={this}/>

                <div className={this.state.toggleRepo ? "base--disabled" : "base" }>
                    <form method="post" encType="multipart/form-data">
                        <input type="hidden" name="product" value={this.props.parent.state.product.post.id} />
                        {/* <!-- IMAGE SELECT AREA--> */}

                        <div className="form__image">
                            <div id="img_select">
                                <div id="img_select__img" className="repoImagePreview">
                                    <input type="hidden" id="art_selected_image" name="image" />
                                </div>

                                <div id="img_select__buttons">
                                    <div className="btnIcon_1" onClick={() => { this.toggleRepo() }}>
                                        <div className="btnIcon_1__icon">
                                            <svg className="icon">
                                                <use xlinkHref="#repo" />
                                            </svg>
                                        </div>
                                        <div className="btnIcon_1__label f_button_2 f_text-capitalize">Repo</div>
                                    </div>
                                </div>

                            </div>

                        </div>

                        {/* <!-- IMAGE SELECT AREA--> */}

                        <div className="form__box">
                            {/* <!-- ARTICLE TITLE AREA--> */}
                            <div className="form__title">
                                <TextInput 
                                    parent={this} 
                                    status={0}
                                    config={{
                                        text: "",
                                        label: "Title",
                                        type: "text_input_4",
                                        comment:"Maximum characters allowed is (80). Currently, its ( "+ this.state.form.title.value.length + " )",
                                        inputValue:""
                                    }} />

                            </div>
                            {/* <!-- ARTICLE TITLE AREA--> */}



                            {/* <!-- ARTICLE TEXT AREA--> */}
                            <div className="form__textBox">
                                <div className="form__textBox__label f_label_1 f_text-capitalize">Body</div>
                                <div className="form__textBox__input ck--1">
                                    <CKEditor
                                        editor={BalloonEditor}
                                        data={this.state.form.body}
                                        onChange={this.handleProductBodyChange}
                                    />
                                </div>
                                <div className="comment f_comment_1 f_text-capitalize">Maximum characters allowed is (60000). Currently, its ( {this.state.form.body.length} )</div>
                            </div>
                            {/* <!-- ARTICLE TEXT AREA--> */}



                            {/* <!-- ARTICLE SUMMARY AREA--> */}
                            <div className="form__summaryBox">
                                <MultiLineText
                                    parent={this}
                                    status={0}
                                    config={{
                                        text: "",
                                        label: "Summary",
                                        type: "mul_text_input",
                                        comment: "Maximum characters allowed is (200). Currently, its ( " + this.state.form.summary.value.length + " )",
                                        inputValue: this.state.form.summary.value
                                    }} />

                            </div>
                            {/* <!-- ARTICLE SUMMARY AREA--> */}



                            <div className="form__tagInput">
                                <div className="form__tagInput__label f_label_1 f_text-capitalize">Tags</div>
                                <div className="form__tagInput__input" >
                                    <TagInput main={this.state.parent} parent={this} />
                                </div>
                            </div>


                            <div className="form__buttons">
                                <div className="form__buttons__button">
                                    <Button parent={this} status={0} config={{
                                        label: "Save",
                                        action: this.product_submit,
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>

                                <div className="form__buttons__button">
                                    <Button parent={this} status={0} config={{
                                        label: "Back",
                                        action: () => {
                                            parent.setView(1)
                                        },
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>
                            </div>

                        </div>
                    </form>
                </div>

                {this.loadRepo()}
            </div>
        );
    }
}

export default Products;
import React from 'react';
import ReactDOM from 'react-dom';
import AccountsView from '../../components/Admin/accounts';

ReactDOM.render( 
    <AccountsView view={[1,0,0]}/> ,
    document.getElementById('accountsViewComponent')
);
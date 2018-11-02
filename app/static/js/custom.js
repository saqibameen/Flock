// Add hashtags.
let addHashtag = () =>  {
    let hashtagInput = document.getElementById('newHashtag');
    // If it's empty return.
    if (hashtagInput.value.trim() == '') {
        return;
    };

    // Regex to check for the valid hashtag
    const regex = /^((?!\s)_?[A-Za-z0-9]\w*\b)/;

    if (hashtagInput.value.match(regex)) { // If valid.
        // Create new element with the hashtag.
        let newEntry = document.createElement('li');
        newEntry.classList.add("hashtag");
        newEntry.innerHTML = hashtagInput.value.trim() + '&nbsp; <span class="cross" onclick="removeHashtag(this)">x</span>';
        // Insert the element.
        document.getElementById('hashtag-container').appendChild(newEntry);
        // Clear the input field.
        hashtagInput.value = '';
    } else {
        alert('Enter a valid hashtag');
    }
}

// Remove the hashtag from DOM.
let removeHashtag = (el) => {
    el.parentElement.remove();
}

// Function to update/save hashtags.
let saveHashtags = () => {
    // Grab the current hashtags.
    let els = document.getElementsByClassName('hashtag');
    let text = [];
    // Grab each hashtag and store in list.
    for (let el of els){
        let m = el.innerText.split(' ')[0].trim();
        if (m != 'x') {
            text.push(m);
        }
        
    }
    let dbString = text.join(); // Join (by default by comma) to store in db.
    
    // Ajax call to store.
    $.ajax({
        url: '/saveHashtags',
        data: {
            hashtags: dbString,
        },
        type: 'POST',
        success: function(response) {
            // Display success message.
            document.getElementById("success").innerHTML = 'Successfully Added!';
            setTimeout(function(){
                document.getElementById("success").innerHTML = '';
            }, 3000);
        },
        error: function(error) {
            document.getElementById("error").innerHTML = 'Error occurred. Try Again!';
            setTimeout(function(){
                document.getElementById("error").innerHTML = '';
            }, 3000);
        }
    });
}


// Unlink the twitter account.
let unlinkAccount = (accId, el) => {
    // Do an ajax request to delete the account.
    $.ajax({
        url: '/unlinkAccount',
        data: {
            twitter_id: accId,
        },
        type: 'POST',
        success: function(response) {
            el.parentElement.parentElement.remove(); // Remove the account from display.
            // Show the response message.
            document.getElementById("success").innerHTML = 'Successfully Deleted!';
            setTimeout(function(){
                document.getElementById("success").innerHTML = '';
            }, 3000);
        },
        error: function(error) {
            // Error.
            document.getElementById("error").innerHTML = 'Error occurred. Try Again!';
            setTimeout(function(){
                document.getElementById("error").innerHTML = '';
            }, 3000);
        }
    });
}

// Do the search.
let searchAjax = () => {
    // Get the element by id.
    let el= document.getElementById('search-query')
    let query = el.value.trim(); // Grab input value.
    
    // Ajax to do the search.
    $.ajax({
        url: '/searchHashtags',
        data: {
            query: query,
        },
        type: 'POST',
        success: function(response) {
            // Remove the current tags.
            let rem = document.getElementById('hashtag-container-search');
            if (rem){
                rem.remove();
            }
            // Create new element and add classes.
            let newEl = document.createElement('ul');
            newEl.classList.add('hashtag-container-main');
            newEl.id = 'hashtag-container-search';
            document.getElementById('retweet-hashtag-container').appendChild(newEl);
            // Tranverse the response and dump into container.
            let jsonResponse = JSON.parse(response);
            if (jsonResponse['hashtags'].length > 0) {
                for (let itr of jsonResponse['hashtags']) {
                    let entry = document.createElement('li');
                    entry.innerText = itr[0];
                    entry.classList.add('hashtag-main');
                    newEl.appendChild(entry);
                }
            } else { // If no result then error.
                let entry = document.createElement('li');
                entry.innerText = 'No Result Found';
                newEl.appendChild(entry);
            }

        }, // Error.
        error: function(error) {
            let rem = document.getElementById('hashtag-container-search');
            if (rem){
                rem.remove();
            }
            let newEl = document.createElement('p');
            package.innerText('No Result Found');
            newEl.classList.add('hashtag-container-main');
            newEl.id('hashtag-container-search');
            document.getElementById('retweet-hashtag-container').appendChild(newEl); 
        }
    });
}



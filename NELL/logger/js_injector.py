js = """
(function() {
    if (window.myAppInstrumented) return;
    window.myAppInstrumented = true;

    window.processingEnterKey = false;

    function sendLogToServer(logData) {
        let logs = JSON.parse(localStorage.getItem('logs') || '[]');
        logs.push(logData);
        localStorage.setItem('logs', JSON.stringify(logs));

        fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(logs),
            mode: 'no-cors'
        }).catch(error => {
            console.error('Error sending logs:', error);
        });
    }

    function findXPath(element) {
        if (element.id !== '')  return 'id("${element.id}")';        
        if (element === document.body)  return '/html/' + element.tagName.toLowerCase();
        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) 
                return findXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
        }
    }
        
    function setUpEventListeners() {
    
        document.addEventListener('click', function(event) {
            if (window.processingEnterKey) {
                return;
            }
            let element = event.target;
            let tagName = element.tagName.toLowerCase();
            
            let detail = tagName === 'button' ? 'text: ' + element.innerText : 'value: ' + element.value;     
            log = {
                event: 'click', 
                tagName: tagName
            }

            let uid = element.getAttribute('uid'); 
            if(uid==None) log['widget_id'] = uid;
            else log['xpath'] = findXPath(element);
            sendLogToServer(log);
            
        });
        
        document.addEventListener('keydown', function(event) {
            if ((event.key === 'Enter' || event.key === 'Tab') && !window.processingEnterKey) {
                window.processingEnterKey = true;
                let element = event.target;
                let tagName = element.tagName.toLowerCase();
                
                 log = {
                    event: 'sendkeys', 
                    tagName: tagName, 
                    text: element.value,
                    specialKey: event.key
                }
                
                let uid = element.getAttribute('uid'); 
                if(uid==None) log['widget_id'] = uid;
                else log['xpath'] = findXPath(element);
                sendLogToServer(log);
                
                setTimeout(function() {
                    window.processingEnterKey = false;
                }, 0);
            }
        });
    }
    setUpEventListeners();

    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                setUpEventListeners();
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();
"""
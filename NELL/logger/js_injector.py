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

    function setUpEventListeners() {
        document.addEventListener('click', function(event) {
            if (window.processingEnterKey) {
                return;
            }
            let element = event.target;
            let tagName = element.tagName.toLowerCase();
            let detail = tagName === 'button' ? 'text: ' + element.innerText : 'value: ' + element.value;
            sendLogToServer({event: 'click', tagName: tagName, widget_id: element.getAttribute('key')});
        });

        document.addEventListener('keydown', function(event) {
            if ((event.key === 'Enter' || event.key === 'Tab') && !window.processingEnterKey) {
                window.processingEnterKey = true;
                let element = event.target;
                let tagName = element.tagName.toLowerCase();
                sendLogToServer({
                    event: 'sendkeys', 
                    tagName: tagName, 
                    widgwt_id: element.getAttribute('key'), 
                    text: element.value,
                    specialKey: event.key
                });
                setTimeout(function() {
                    window.processingEnterKey = false;
                }, 0);
            }
        });

        // Se necessário, adicione o blurListener
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
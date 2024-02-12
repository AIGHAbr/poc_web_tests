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
            body: JSON.stringify(logData),
            mode: 'no-cors'
        }).catch(error => {
            console.error('Error sending logs:', error);
        });
    }

    
    function findXPath(element, isRecursive = false) {
        if (element === document.body) return '/html/body';
        if (element.id !== '') return `//*[@id="${element.id}"]`;

        if (!isRecursive) {
            let linkElement = element.closest('a');
            if (linkElement) {
                let href = linkElement.getAttribute('href');
                if (href) {
                    // Constrói e retorna o XPath para o primeiro <a> com o href específico
                    return `//a[@href="${href}"]`;
                }
            }
        }

        if (!isRecursive) {
            let selectors = ['span', 'b', 'a', 'p', 'h1', 'h2', 'h3', 'label', 'input', 'button', 'img', 'div', 'section'];
            for (let selector of selectors) {
                const child = element.querySelector(selector);
                if (child) {
                    let attribute = '';
                    const text = child.textContent.trim();
                    if (text) attribute = `contains(text(), "${text}")`;
                    if (attribute) {
                        return `${findXPath(element.parentNode, true)}//${selector}[${attribute}]`;
                    }
                }
            }
        }

        let position = 1;
        let siblings = element.parentNode.children;
        for (let sibling of siblings) {
            if (sibling === element) break;
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) position++;
        }
        return `${findXPath(element.parentNode, true)}/${element.tagName.toLowerCase()}[${position}]`;
    }


        
    function setUpEventListeners() {
    
        document.addEventListener('click', function(event) {
            if (window.processingEnterKey) {
                return;
            }
            let element = event.target;
            let tagName = element.tagName.toLowerCase();
            let log = {
                event: 'click', 
                tagName: tagName
            }

            let uid = element.getAttribute('uid'); 
            if(uid) {
                log['widget_id'] = uid;
                sendLogToServer(log);
                return;
            }
            log['xpath'] = findXPath(element);
            if(log['xpath'].startsWith("//a[")) 
                log['tagName'] = 'a';

            sendLogToServer(log);
            
        });
        
        document.addEventListener('keydown', function(event) {
            if ((event.key === 'Enter' || event.key === 'Tab') && !window.processingEnterKey) {
                window.processingEnterKey = true;
                let element = event.target;
                let tagName = element.tagName.toLowerCase();
                
                let log = {
                    event: 'sendkeys', 
                    tagName: tagName, 
                    text: element.value,
                    specialKey: event.key
                }
                
                let uid = element.getAttribute('uid'); 
                if(uid) log['widget_id'] = uid;
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
url  = "https://docs.google.com/forms/d/e/1FAIpQLSfgke5tW8u87C-CRGITf76JS3K6-2_FGFgnm7iYYc1zOnAFow/viewform"

webdriver_directory = 'D:\MyDocument\Software\software\Exe file\chromedriver.exe'


#command to input into broswer console
command = '''
    function loop(e) {
        if (e.children)
        for (let i=0; i < e.children.length; i++) {
            let c = e.children[i], n = c.getAttribute('name');
            if (n) console.log(`${c.getAttribute('aria-label')}: ${n}`);
            loop(e.children[i]);}
    }; loop(document.body); 
    '''



def page_down(driver):
    driver.execute_script('''
                            const scrollStep = 200; // Размер шага прокрутки в пикселях
                            const scrollInterval = 300; // Интервал между шагами в милисекундах
                            
                            var scrollHeight = document.documentElement.scrollHeight;
                            let currentPosition = 0;
                            const interval = setInterval(() => {
                                    window.scrollBy(0, scrollStep);
                                    currentPosition += scrollStep;
                                    scrollHeight = document.documentElement.scrollHeight;
                                    
                                    if(currentPosition >= scrollHeight) {
                                        clearInterval(interval);
                                    }
                                }, scrollInterval);
                        ''')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:17:54 2019

@author: Zane Jakobs
@brief: file contains standardization guidelines, class and function headers
that have not been implemented but need to/should be, and general notes
for writing good scientific code.
"""


'''
STANDARD GUIDELINES:
    
    GENERAL GUIDELINES:
        
        I'll update this section as I think of more stuff. Likewise, if you have
        style tips for scientific programming that I left out, feel free to add
        them here.
        
        Prefer modular code. A function should perform one primary task, not 
        several. It's much easier to read and reason about a sequence of function 
        calls, where each function does one thing, than to try and decompose
        one single function that does several things. 
        
        Make code maximally generic. If you can write a function that works for
        multiple types instead of one with minimal or no no performance or 
        implementation complexity penalty, do that For example, in the HW 
        assignment to write an IRLS solver (see the code on my GitHub,
        www.github.com/diffeoInvariant),the solve function loops, updating beta
        until convergence. Instead of writing this as one function, consider
        writing a loop that takes in a function that depends of the type of
        regression you're running (L1, L2, LP for p >2, Ridge regression,LASSO, 
        etc.) or selects one based on the state of the program 
        (e.g. a class instance variable). The same solve function can 
        now handle any type of regression that you can write an inner loop
        function (that is, a function to update beta) for.  
        
        Put each class into its own file containing the class and any functions
        designed to operate on instances of that class, or that are related 
        to that class only (and not to the rest of the program). General utility
        functions and functions that aren't specific to a certain class go 
        in the utility file. 
    
    DATATYPES:
        All matrix data is to be stored in a numpy array/matrix (type numpy.ndarray)
        or a Pandas DataFrame. Prefer numpy arrays/matrices to DataFrames
        for code that has to run fast. Prefer DataFrames where ease of accessibility
        and mutation/filtering of data is most important. Only use a different 
        container for array-like data if absolutely necessary, and clearly
        document the need. If you call a library function that outputs a matrix
        or array of a different type, cast it to either a numpy array or a Pandas
        DataFrame.
        
        Prefer (pseudo-)statically sized containers over dynamically sized,
        especially where speed is important. The "pseudo-" is because since this 
        is Python, even the static-looking containers like numpy arrays can be
        resized. In general, prefer static memory over dynamic memory for both 
        speed and safety.
        
    LIBRARIES:
        Prefer base Python where convenient, and numpy for fast computation. 
        Use the fewest number of libraries needed to efficiently accomplish 
        your task. If the same functionality exists in two different libraries, 
        but one is already used in the file you're writing, use that instead 
        of importing a new library.
        
    JIT COMPILATION:
        Python is an interpreted language, but that doesn't mean we can't use
        a just-in-time (JIT) compiler; specifically, at the top of each file 
        using JIT compilation, make the import call
        
        from numba import jit
        
        . If you don't know what that is, go Google
        it. If your function doesn't call any fancy library functions (for example,
        a plotting function that uses matplotlib.pyplot), put an @jit wrapper above
        it. Example, bad:
            
            def bigLoopFunc():
                #code
                
        Example, good:
            
            @jit
            def bigLoopFunc():
                #code
                
    DOCUMENTATION:
        Document function definitions like so:
            
            ### (for actual code, use triple apostrophes, but you can't do that 
            inside another block comment)
            @author: Zane Jakobs
            @brief: Fits OLS regression
            @param X: data matrix (predictors)
            @param y: observed data (target)
            @return: OLS-optimal betas (regression parameters)
            ### (end of block comment)
            def OLSFit(X,y):
                #code
                
        If multiple people contribute to writing the same function/class, 
        use multiple author lines.
        
    CODE REVIEW: 
        USE THE PROJECT SECTION ON GITHUB. WHEN YOU'VE FINISHED WRITING A FILE, PLACE THAT FILE IN THE
        TESTING SECTION ALONG WITH UNIT TESTS FOR IT. ONE OTHER PERSON (ANYBODY CAN DO THIS) SHOULD THEN PERFORM THE 
        UNIT TESTS ON THEIR MACHINE, VERIFY THAT THE OUTPUT IS CONSISTENT WITH THE SPECIFICATIONS, AND ADD THE FILE
        TO THE READY TO COMMIT SECTION. WHEN WE HAVE FINISHED A PARTCULAR CHUNK OF THE PROJECT, WE'LL PUSH THE FILES
        TO THE MAIN BRANCH.
'''

'''
TO-DO LIST FOR WEEK OF 4/8/19:
    
    Let me know if the requirements are too vague or you need more information
    for a task you've signed up for, and I'll try to clarify. -Zane
    
    DATA IMPORT:
        WHO'S DOING IT: YOUR NAME HERE IF YOU WANT TO DO THIS (MULTIPLE PEOPLE
        CAN WORK ON THE SAME THING)
        TASK:
            Write a class or functions (if you're not sure which to use,
            ask me; I'm leaving it open here because depending on how you want 
            to implement this, either way could end up being better) to read in
            the historical and forecasted data. There should be one function that
            (through a sequence of calls to other functions, as usual) does 
            ALL of the following:
                1. READ IN HISTORICAL DATA FROM PROJECT REPO
                2. CLEAN HISTORICAL DATA (ensure that there are no NaN's,
                that all time series are the same length, and, if they have 
                dates associated with the datapoints, that they start on the 
                same day.)
                3. LOAD HISTORICAL PRICE DATA INTO A PANDAS DATAFRAME, WITH 
                EACH COLUMN LABEL BEING THE STOCK'S TICKER (e.g. AAPL), AND 
                ENTRIES BEING PRICES
                4. LOAD HISTORICAL DAILY RETURNS INTO A DIFFERENT PANDAS DATAFRAME
                WITH THE SAME COLUMN NAMING RULES AS ABOVE. YOU MAY ASSSUME
                THE EXISTENCE OF FUNCTIONS WITH THE FOLLOWING SIGNATURES
                (I'm going to write them):
                    
                    @param price_series: numeric vector of prices
                    @return: numeric vector of returns, excluding the first
                    date in the price series (differencing shortens the series
                    by 1 observation).
                    def price_to_daily_returns(price_series)
                    
                    
                    @param returns: numeric vector of returns
                    @param init_price: initial price of the security
                    @return: price series of the security (by integrating returns)
                    def daily_returns_to_price(returns)
                5. LOAD FACTOR DATA INTO A THIRD PANDAS DATAFRAME, WHERE THE 
                LEFTMOST COLUMN CONTAINS THE MARKET'S RETURNS, THE NEXT ONE TO
                THE RIGHT CONTAINS THE TRADING VOLUME OF THE MARKET, AND THE 
                REMAINING COLUMNS CONTAIN FACTOR DATA FOR EACH INDIVIDUAL STOCK,
                WITH THE SAME NAMING RULES WE'VE BEEN USING. IF I HAVEN'T UPLOADED
                THE FACTOR DATA TO GITHUB, DON'T DO THIS STEP (TALK TO ME IF
                YOU'RE NOT SURE).
                6. PERFORM STEPS 1-5 WITH THE FORECAST DATA
                7. RETURN EITHER THE RESULT OF JOINING THE DATAFRAMES IN A
                MANNER THAT MAKES SENSE (I DON'T SEE WHAT SUCH A MANNER WOULD BE
                FOR THIS DATA, BUT IF YOU FIND ONE AND PREFER THIS TO THE NEXT 
                OPTION, GO AHEAD AND DO IT) OR RETURN A DICTIONARY WHOSE KEYS ARE
                'HistoricalPrice', 'HistoricalRet','HistoricalFactor'
                (iff step 5 applies), 'ForecastPrice', 'ForecastRet', and
                'ForecastFactor' (iff step 5 applies).
                
            Once you've done that, write a function to do the following:
                1. READ IN HI80 AND LO80 DATA FROM THE ARIMAX FORECASTS AND 
                HISTORICAL FITS CURRENTLY IN THE PROJECT REPO. FOR EACH
                SECURITY ON DAY i, DEFINE THE STANDARD DEVIATION OF PRICE
                FOR (the time up to) THAT DAY TO BE HI80[i] - LO80[i]. THIS
                IS JUST A WORK-AROUND UNTIL I CAN GET GOOD SIMULATIONS
                TO FIND A MORE ACCURATE ESTIMATOR OF THE VARIANCE.
                
    DATA SELECTION:
        WHO'S WORKING ON THIS: ZANE JAKOBS, YOUR NAME HERE IF YOU WANT TO WORK ON THIS.
        
        SELECT WHICH SECURITIES TO PASS TO THE OPTIMIZER. THIS SHOULD BE ONES THAT
        WE THINK WILL GO UP A LOT OR DOWN A LOT, SO TAKING A POSITION IN THEM
        SHOULD BE PROFITABLE
    
 
                
    LINEAR OPTIMIZATION:
        WHO'S WORKING ON THIS: YOUR NAME HERE (SETUP SECTION), ZANE JAKOBS (SOLVER SECTION)
        
        NOTE THAT IF YOU SEE A BETTER WAY TO DO THE LINEAR OPTIMIZATION PART,
        FEEL FREE TO REPLACE THIS MODEL SPECIFICATION WITH YOUR OWN
        
        SETUP SECTION:
        Define the following variables:
            V0 is total portfolio initial value. V0*leverage is the upper bound
            on what we can spend.
            
            leverage: ( [TOTAL OWNED CAPITAL] + [TOTAL AMOUND BORROWED])/[TOTAL OWNED CAPITAL]
            
            w is the vector of weights applied to each security. If, say, 
            w[i] = +7.1e-2, then we buy 7.1e-2 * V0 dollars worth of that security.
            If w[i] were to equal, say, -0.013, then we should short 0.013*V0 
            dollars worth of that security.
            
            r is the vector of returns of each security over the time period 
            we're optimizing for (so for security i, r[i] is the price of security
            i at the end of the time period (if the end is in the future,
            then it's the forecast price) minus the price of the same security
            at the beginning, divided by the price at the beginning). 
            
            sd is the vector of standard deviations for each security in the same
            way as r is for the returns. The ratio r[i]/sd[i] is the security's
            Sharpe ratio over the period
            
            p0 is the vector of initial prices of each security
            
            max_dollar_exposure is the maximum market beta we will use, defined as the 
            total number of dollars in long positions minus the total number
            of dollars in short positions, divided by V0.
            This will form a constraint.
            
            The simplest optimization we can do--note that this completely ignores portfolio level risk--is then
            
                Max w^T * (r[i]/sd[i]) over values of w (NOTE: WE CAN USE JUST r[i] IF YOU WANT, AND WE SHOULD DO BOTH)
                s.t.
                
                1^T * w <= dollar_exposure
                1^T * w >=  -dollar_exposure
                sum of | w[i] | over i = leverage
                
     
    SOLVER SECTION:
    (I'll do this--Zane)
    Choose an existing linear solver or roll your own (almost certainly, an existing one will be fine). Verify that the input is 
    in the correct form to optimize, optimize it, and display the results
            
            
            
                



'''

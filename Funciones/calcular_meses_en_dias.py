def is_year_leap(year):
    
    if (year%4 == 0) and (year%100 != 0):
        return True
    elif (year%4 == 0) and (year%100 == 0) and (year%400 == 0):
        return True
    elif (year%100 == 0) and (year%400 == 0):
        return True
    else:
        return False

def days_in_month(year, month):

    month_days = [31, [28, 29], 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    is_bisiesto = is_year_leap(year)

    if (is_bisiesto == True) and (month == 2):
        return month_days[1][1]
    
    elif (is_bisiesto == False) and (month == 2):
        return month_days[1][0]
    else:
        return month_days[month - 1]

test_years = [1900, 2000, 2016, 1987]
test_months = [2, 2, 1, 11]
test_results = [28, 29, 31, 30]
for i in range(len(test_years)):
    yr = test_years[i]
    mo = test_months[i]
    print(yr, mo, "->", end="")
    result = days_in_month(yr, mo)
    if result == test_results[i]:
        print("OK")
    else:
        print("Fallido")
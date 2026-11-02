def is_year_leap(year):
    
    if (year%4 == 0) & (year%100 != 0):
        return True
    elif (year%4 == 0) & (year%100 == 0) & (year%400 == 0):
        return True
    elif (year%100 == 0) & (year%400 == 0):
        return True
    else:
        return False

def days_in_month(year, month):

    month_days = [1, [28, 29], 3, 4, 31, 30, 31, 31, 30, 31, 30, 31]

    is_bisiesto = is_year_leap(year)

    if is_bisiesto == True & month == 2:
        print(f"{month_days[1][1]}")
        return month_days[1][1]
    
    elif is_bisiesto == False & month == 2:
        print(f"{month_days[1][0]}")
        return month_days[1][0]
    
    else:
        print(f"{month_days[month]}")
        return month_days[month]

for month in [1, [28, 29], 3, 4, 31, 30, 31, 31, 30, 31, 30, 31]:
    print(f"{month}")

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
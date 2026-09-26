s = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        return True, f'выходной ({names[d.weekday()]})'
    easter = _easter_date(d.year)
    good_friday = easter - _dt.timedelta(days=2)
    easter_monday = easter + _dt.timedelta(days=1)
    fixed = {
        _dt.date(d.year, 1, 1): "New Year's Day",
        good_friday: 'Good Friday',
     
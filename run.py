import gobject


def d():
    print "Hola"
    return True
gobject.timeout_add(100, d)
gobject.init_threads()

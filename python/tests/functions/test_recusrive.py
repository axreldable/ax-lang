from tests.test_utils import exec_test


def test_factorial(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (def factorial (x)
            (if (== x 1)
                1
                (* x (factorial (- x 1)))))
    
        (factorial 5)
    )
    """,
        120,
    )


def test_callback(ax_lang):
    exec_test(
        ax_lang,
        """
    (begin
        (def createCallback (x)
            (lambda (y) (+ x y)))
            
        (var fn (createCallback 5))
        
        (fn 10)
    )
    """,
        15,
    )

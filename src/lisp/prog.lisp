(label length (lambda (l)
                (prog (u v)
                  (setq v 0)
                  (setq u l)
                a (cond ((null u),(return v)))
                  (setq u (cdr u))
                  (setq v (+ 1 v))
                  (go a)
                )
              )
)
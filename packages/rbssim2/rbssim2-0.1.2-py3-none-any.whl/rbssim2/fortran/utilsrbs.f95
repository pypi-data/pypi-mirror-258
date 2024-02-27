
subroutine gauss(x, lenx, a, b, c, d,  newx)
    
         integer :: lenx
         real(8) :: x(lenx), newx(lenx)
         real(8) :: a, b, c, d
!f2py    intent(in) x, a, b, c, d, lenx
!f2py    intent(out) newx
!f2py    depend(lenx) x, newx


!$OMP PARALLEL
    newx = a * exp( - 0.5 * ( x - b) ** 2 / (c ** 2)) + d
!$OMP END PARALLEL
    
end subroutine gauss


subroutine get_spread_responce(energies, spreads, size, kinfactor, matrix)

        integer :: size
        real(8) :: energies(size), newspreads(size), spreads(size), kinfactor
        real(8) :: matrix(size, size), row(size), a, d
        a = 1.
        d = 0.
!f2py   intent(in) energies, spreads, size, kinfactor
!f2py   intent(out) matrix
!f2py   depend(size) energies, spreads
        matrix(1, 1) = 1
        newspreads = spreads + spreads * kinfactor ** 2
        newspreads = sqrt(newspreads)

!$OMP PARALLEL
        do i = 2, size
            call gauss(energies, size, a, energies(i), newspreads(i), d, row)
            row = row / sum(row)
            matrix(i, :) = row
        enddo

end subroutine get_spread_responce
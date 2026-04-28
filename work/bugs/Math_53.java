    /**
     * Return the sum of this complex number and the given complex number.
     * <p>
     * Uses the definitional formula
     * <pre>
     * (a + bi) + (c + di) = (a+c) + (b+d)i
     * </pre></p>
     * <p>
     * If either this or <code>rhs</code> has a NaN value in either part,
     * {@link #NaN} is returned; otherwise Infinite and NaN values are
     * returned in the parts of the result according to the rules for
     * {@link java.lang.Double} arithmetic.</p>
     *
     * @param rhs the other complex number
     * @return the complex number sum
     * @throws NullArgumentException if <code>rhs</code> is null
     */
    public Complex add(Complex rhs)
        throws NullArgumentException {
        MathUtils.checkNotNull(rhs);
-        return createComplex(real + rhs.getReal(),
-            imaginary + rhs.getImaginary());
+	if ((isNaN) || (rhs.isNaN)) {
+            return NaN;
+        }
+        return createComplex((real) + (rhs.getReal()),
+            (imaginary) + (rhs.getImaginary()));
    }

    /**
     * Return the conjugate of this complex number. The conjugate of
     * "A + Bi" is "A - Bi".
     * <p>
     * {@link #NaN} is returned if either the real or imaginary
     * part of this Complex number equals <code>Double.NaN</code>.</p>
     * <p>
     * If the imaginary part is infinite, and the real part is not NaN,
     * the returned value has infinite imaginary part of the opposite
     * sign - e.g. the conjugate of <code>1 + POSITIVE_INFINITY i</code>
     * is <code>1 - NEGATIVE_INFINITY i</code></p>
     *
     * @return the conjugate of this Complex object
     */
    public Complex conjugate() {
        if (isNaN) {
            return NaN;
        }
-        return createComplex(real, -imaginary);
+        return createComplex(real, (-(imaginary)));
    }

    /**
     * Return the quotient of this complex number and the given complex number.
     * <p>
     * Implements the definitional formula
     * <pre><code>
     *    a + bi          ac + bd + (bc - ad)i
     *    ----------- = -------------------------
     *    c + di         c<sup>2</sup> + d<sup>2</sup>
     * </code></pre>
     * but uses
     * <a href="http://doi.acm.org/10.1145/1039813.1039814">
     * prescaling of operands</a> to limit the effects of overflows and
     * underflows in the computation.</p>
     * <p>
     * Infinite and NaN values are handled / returned according to the
     * following rules, applied in the order presented:
     * <ul>
     * <li>If either this or <code>rhs</code> has a NaN value in either part,
     *  {@link #NaN} is returned.</li>
     * <li>If <code>rhs</code> equals {@link #ZERO}, {@link #NaN} is returned.
     * </li>
     * <li>If this and <code>rhs</code> are both infinite,
     * {@link #NaN} is returned.</li>
     * <li>If this is finite (i.e., has no infinite or NaN parts) and
     *  <code>rhs</code> is infinite (one or both parts infinite),
     * {@link #ZERO} is returned.</li>
     * <li>If this is infinite and <code>rhs</code> is finite, NaN values are
     * returned in the parts of the result if the {@link java.lang.Double}
     * rules applied to the definitional formula force NaN results.</li>
     * </ul></p>
     *
     * @param rhs the other complex number
     * @return the complex number quotient
     * @throws NullArgumentException if <code>rhs</code> is null
     */
    public Complex divide(Complex rhs)
        throws NullArgumentException {
        MathUtils.checkNotNull(rhs);
-        if (isNaN || rhs.isNaN) {
+        if ((isNaN) || (rhs.isNaN)) {
            return NaN;
        }

        double c = rhs.getReal();
        double d = rhs.getImaginary();
        if (c == 0.0 && d == 0.0) {
            return NaN;
        }

        if (rhs.isInfinite() && !isInfinite()) {
            return ZERO;
        }

        if (FastMath.abs(c) < FastMath.abs(d)) {
            double q = c / d;
            double denominator = c * q + d;
            return createComplex((real * q + imaginary) / denominator,
                (imaginary * q - real) / denominator);
        } else {
            double q = d / c;
            double denominator = d * q + c;
            return createComplex((imaginary * q + real) / denominator,
                (imaginary - real * q) / denominator);
        }
    }

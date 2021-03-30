public class ArithmeticsDiv implements IArithmeticsDiv {

    @Override
    public double division(double A, double B) {
        if (B!=0)
            return A / B;
        else
            return 0;
    }
}

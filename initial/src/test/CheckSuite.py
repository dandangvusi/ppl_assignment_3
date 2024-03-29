import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):
    def test_1(self):
        """Test undeclared function"""
        input = Program([FuncDecl(Id("main"),[],([],[
            CallExpr(Id("foo"),[])]))])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_2(self):
        """Test different number of param in call expression"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[
                        CallExpr(Id("read"),[IntLiteral(4)])
                        ])]))])
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_3(self):
        """Test different number of param in call statement"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_4(self):
        """Test no entry point"""
        input = Program([FuncDecl(Id("add_one"),[VarDecl(Id("n"),[],None)],([],[Return(BinaryOp("+",Id("n"),IntLiteral(1)))]))])
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_5(self):
        """Test redeclared global variable"""
        input = Program([VarDecl(Id("x"),[],IntLiteral(10)),VarDecl(Id("x"),[],IntLiteral(20)),
                              FuncDecl(Id("main"),[],
                                ([VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],
                                 [Assign(Id("a"),BinaryOp("+",Id("x"),Id("y"))),
                                  Assign(Id("b"),BinaryOp("*",IntLiteral(2),Id("y")))]))])
        expect = str(Redeclared(Variable(), "x"))
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_6(self):
        """Test redeclared local variable"""
        input = Program([VarDecl(Id("x"),[],IntLiteral(10)),VarDecl(Id("y"),[],IntLiteral(20)),
                              FuncDecl(Id("main"),[],
                                ([VarDecl(Id("a"),[],None),VarDecl(Id("a"),[],None)],
                                 [Assign(Id("a"),BinaryOp("+",Id("x"),Id("y"))),
                                  Assign(Id("b"),BinaryOp("*",IntLiteral(2),Id("y")))]))])
        expect = str(Redeclared(Variable(), "a"))
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_7(self):
        """Test redeclared global variable"""
        input = Program([VarDecl(Id("x"),[],None),VarDecl(Id("x"),[],IntLiteral(20)),
                              FuncDecl(Id("main"),[],
                                ([VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],
                                 [Assign(Id("a"),BinaryOp("+",Id("x"),Id("y"))),
                                  Assign(Id("b"),BinaryOp("*",IntLiteral(2),Id("y")))]))])
        expect = str(Redeclared(Variable(), "x"))
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_8(self):
        """Test redeclared global variable"""
        input = Program([VarDecl(Id("x"),[],None),VarDecl(Id("x"),[],None),
                              FuncDecl(Id("main"),[],
                                ([VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],
                                 [Assign(Id("a"),BinaryOp("+",Id("x"),Id("y"))),
                                  Assign(Id("b"),BinaryOp("*",IntLiteral(2),Id("y")))]))])
        expect = str(Redeclared(Variable(), "x"))
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_9(self):
        """Test redeclared global variable"""
        input = Program([VarDecl(Id("x"),[],IntLiteral(10)),VarDecl(Id("x"),[],None),
                              FuncDecl(Id("main"),[],
                                ([VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],
                                 [Assign(Id("a"),BinaryOp("+",Id("x"),Id("y"))),
                                  Assign(Id("b"),BinaryOp("*",IntLiteral(2),Id("y")))]))])
        expect = str(Redeclared(Variable(), "x"))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_10(self):
        """Test redeclared local variable"""
        input = Program([VarDecl(Id("x"),[],IntLiteral(10)),VarDecl(Id("y"),[],IntLiteral(20)),
                              FuncDecl(Id("main"),[],
                                ([VarDecl(Id("a"),[],None),VarDecl(Id("a"),[],IntLiteral(2))],
                                 [Assign(Id("a"),BinaryOp("+",Id("x"),Id("y"))),
                                  Assign(Id("b"),BinaryOp("*",IntLiteral(2),Id("y")))]))])
        expect = str(Redeclared(Variable(), "a"))
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_11(self):
        """Test redeclared param"""
        input = Program([
            FuncDecl(Id("add"),[VarDecl(Id("a"),[],None),VarDecl(Id("a"),[],None)],([],[Return(BinaryOp("+",Id("a"),Id("b")))]))
            ,FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5)),VarDecl(Id("y"),[],IntLiteral(10))],
            [CallStmt(Id("print"),[CallExpr(Id("add"),[Id("x"),Id("y")])])]))])
        expect = str(Redeclared(Parameter(), "a"))
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_12(self):
        """Test redeclared function"""
        input = Program([
            FuncDecl(Id("add"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],([],[Return(BinaryOp("+",Id("a"),Id("b")))])),
            FuncDecl(Id("add"), [VarDecl(Id("a"), [], None), VarDecl(Id("b"), [], None)],
                     ([], [Return(BinaryOp("*", Id("a"), Id("b")))]))
            ,FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5)),VarDecl(Id("y"),[],IntLiteral(10))],
            [CallStmt(Id("print"),[CallExpr(Id("add"),[Id("x"),Id("y")])])]))])
        expect = str(Redeclared(Function(), "add"))
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_13(self):
        """Test redeclared function"""
        input = Program([
            VarDecl(Id("add"),[],IntLiteral(10)),
            FuncDecl(Id("add"), [VarDecl(Id("a"), [], None), VarDecl(Id("b"), [], None)],
                     ([], [Return(BinaryOp("*", Id("a"), Id("b")))]))
            ,FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5)),VarDecl(Id("y"),[],IntLiteral(10))],
            [CallStmt(Id("print"),[CallExpr(Id("add"),[Id("x"),Id("y")])])]))])
        expect = str(Redeclared(Function(), "add"))
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_14(self):
        """Test redeclared param"""
        input = Program([
            FuncDecl(Id("add"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None),VarDecl(Id("a"),[],None)],([],[Return(BinaryOp("+",Id("a"),Id("b")))]))
            ,FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5)),VarDecl(Id("y"),[],IntLiteral(10))],
            [CallStmt(Id("print"),[CallExpr(Id("add"),[Id("x"),Id("y")])])]))])
        expect = str(Redeclared(Parameter(), "a"))
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_15(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(4)),VarDecl(Id("y"),[],None)],
                [Assign(Id("z"),BinaryOp("+",Id("x"),Id("y")))]))])
        expect = str(Undeclared(Identifier(), "z"))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_16(self):
        """Test undeclared parameter"""
        input = Program([
            FuncDecl(Id("add"),[VarDecl(Id("b"),[],None)],([],[Return(BinaryOp("+",Id("a"),Id("b")))]))
            ,FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5)),VarDecl(Id("y"),[],IntLiteral(10))],
            [CallStmt(Id("print"),[CallExpr(Id("add"),[Id("x"),Id("y")])])]))])
        expect = str(Undeclared(Identifier(), "a"))
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_17(self):
        """Test undeclared function"""
        input = Program([
            FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5)),VarDecl(Id("y"),[],IntLiteral(10))],
            [CallStmt(Id("print"),[CallExpr(Id("add"),[Id("x"),Id("y")])])]))])
        expect = str(Undeclared(Function(), "add"))
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_18(self):
        """Test undeclared variable"""
        input = Program([VarDecl(Id("x"),[],None),
            FuncDecl(Id("fact"),[],([],[If([(BinaryOp("==",Id("n"),IntLiteral(0)),[],
            [Return(IntLiteral(1))])],([],[Return(BinaryOp("*",Id("n"),CallExpr(Id("fact"),[BinaryOp("-",Id("n"),IntLiteral(1))])))]))])),
            FuncDecl(Id("main"),[],([],[Assign(Id("x"),IntLiteral(10)),CallStmt(Id("fact"),[Id("x")])]))])
        expect = str(Undeclared(Identifier(), "n"))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_19(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([],
                [Assign(ArrayCell(Id("a"),[IntLiteral(1),IntLiteral(2)]),BinaryOp("-",BinaryOp("*",IntLiteral(4),IntLiteral(5)),IntLiteral(2)))]))])
        expect = str(Undeclared(Identifier(), "a"))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_20(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"),[],None)],
                [If([(CallExpr(Id("bool_of_string"),[StringLiteral("True")]),[],
                [Assign(Id("a"),CallExpr(Id("int_of_string"),[CallExpr(Id("read"),[])])),
                Assign(Id("b"),BinaryOp("+.",CallExpr(Id("float_of_int"),[Id("a")]),FloatLiteral(2.0)))])],
                ([],[]))]))])
        expect = str(Undeclared(Identifier(), "b"))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_21(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [While(BinaryOp("<",Id("x"),BinaryOp("*",IntLiteral(100),IntLiteral(2))),(
                [],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y"))),
                 If([(BinaryOp(">=",Id("x"),IntLiteral(50)),[],[Continue()])],([],[]))]))]))])
        expect = str(Undeclared(Identifier(), "y"))
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_22(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([],
                [Dowhile(([VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]),
                BinaryOp("<",Id("x"),BinaryOp("-",IntLiteral(100),BinaryOp("*",IntLiteral(5),IntLiteral(2)))))]))])
        expect = str(Undeclared(Identifier(), "x"))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_23(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([],
                [Dowhile(([VarDecl(Id("y"),[],IntLiteral(5))],
                []),
                BinaryOp("<",Id("x"),BinaryOp("-",IntLiteral(100),BinaryOp("*",IntLiteral(5),IntLiteral(2)))))]))])
        expect = str(Undeclared(Identifier(), "x"))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_24(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("add_one"),[],([],[Return(BinaryOp("+",Id("n"),IntLiteral(1)))])),
                              FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],[CallStmt(Id("add_one"),[Id("x")])]))])
        expect = str(Undeclared(Identifier(), "n"))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_25(self):
        """Test undeclared variable"""
        input = Program([FuncDecl(Id("main"),[],([],
                [If([(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),IntLiteral(0)),[VarDecl(Id("y"),[],IntLiteral(2)),VarDecl(Id("y"),[],IntLiteral(2))],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1))),Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(0)),[VarDecl(Id("y"),[],IntLiteral(2)),VarDecl(Id("y"),[],IntLiteral(2))],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2))),Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(100)),[VarDecl(Id("y"),[],IntLiteral(2)),VarDecl(Id("y"),[],IntLiteral(2))],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3))),Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([VarDecl(Id("y"),[],IntLiteral(2)),VarDecl(Id("y"),[],IntLiteral(2))],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4))),Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))]))])
        expect = str(Undeclared(Identifier(), "x"))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_26(self):
        """Test undeclared function"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(4)),VarDecl(Id("y"),[],IntLiteral(5)),
                VarDecl(Id("z"),[],IntLiteral(6)), VarDecl(Id("t"),[],None)],
                [Assign(Id("t"),BinaryOp("+",BinaryOp("+",Id("x"),Id("y")),CallExpr(Id("add_one"),[Id("z")])))]))])
        expect = str(Undeclared(Function(), "add_one"))
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_27(self):
        """Test type mismatch in If statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [If([(BinaryOp("%",Id("x"),IntLiteral(2)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(100)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))]))])
        expect = str(TypeMismatchInStatement(If([(BinaryOp("%",Id("x"),IntLiteral(2)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(100)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))))
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_28(self):
        """Test type mismatch in If statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [If([(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (IntLiteral(0),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(100)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))]))])
        expect = str(TypeMismatchInStatement(If([(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (IntLiteral(0),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(100)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_29(self):
        """Test type mismatch in If statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [If([(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (Id("x"),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))]))])
        expect = str(TypeMismatchInStatement(If([(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                     (BinaryOp(">",Id("x"),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                     (Id("x"),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                    ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_30(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],FloatLiteral(5.0))],
                [For(Id("i"),Id("x"),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),Id("x"),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_31(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],FloatLiteral(5.0))],
                [For(Id("i"),FloatLiteral(5.0),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),FloatLiteral(5.0),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_32(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("*.",FloatLiteral(1.0),FloatLiteral(2.0)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("*.",FloatLiteral(1.0),FloatLiteral(2.0)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_33(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("\.",FloatLiteral(1.0),FloatLiteral(2.0)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),IntLiteral(10)),BinaryOp("\.",FloatLiteral(1.0),FloatLiteral(2.0)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_34(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),IntLiteral(10)),FloatLiteral(2.0),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),IntLiteral(10)),FloatLiteral(2.0),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_35(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("+",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(0),BinaryOp("+",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_36(self):
        """Test type mismatch in For statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("%",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(0),BinaryOp("%",Id("i"),IntLiteral(10)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_37(self):
        """Test type mismatch in Array cell"""
        input = Program([FuncDecl(Id("main"), [],
                ([VarDecl(Id("arr"),[3],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])),VarDecl(Id("b"),[],IntLiteral(69))],
                [Assign(ArrayCell(Id("arr"),[FloatLiteral(1.0)]),Id("b"))]))])
        expect = str(TypeMismatchInExpression(ArrayCell(Id("arr"),[FloatLiteral(1.0)])))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_38(self):
        """Test type mismatch in Array cell"""
        input = Program([FuncDecl(Id("main"), [],
                ([VarDecl(Id("arr"),[3],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])),VarDecl(Id("b"),[],FloatLiteral(2.0))],
                [Assign(ArrayCell(Id("arr"),[Id("b")]),IntLiteral(1))]))])
        expect = str(TypeMismatchInExpression(ArrayCell(Id("arr"),[Id("b")])))
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_39(self):
        """Test type mismatch in While statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [While(BinaryOp("+",Id("x"),IntLiteral(100)),(
                [VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]))]))])
        expect = str(TypeMismatchInStatement(While(BinaryOp("+",Id("x"),IntLiteral(100)),(
                [VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]))))
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_40(self):
        """Test type mismatch in While statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [While(Id("x"),(
                [VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]))]))])
        expect = str(TypeMismatchInStatement(While(Id("x"),(
                [VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]))))
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_41(self):
        """Test type mismatch in Binary expression"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],BooleanLiteral(True))],
                [While(Id("x"),(
                [VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("x"),Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_42(self):
        """Test type mismatch assign statement"""
        input = Program([FuncDecl(Id("main"), [],
                ([VarDecl(Id("arr"),[3],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])),VarDecl(Id("b"),[],FloatLiteral(6.9))],
                [Assign(ArrayCell(Id("arr"),[IntLiteral(1)]),Id("b"))]))])
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("arr"),[IntLiteral(1)]),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_43(self):
        """Test type mismatch assign statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [While(BinaryOp("<",Id("x"),BinaryOp("-",IntLiteral(100),BinaryOp("*",IntLiteral(5),IntLiteral(2)))),(
                [VarDecl(Id("y"),[],FloatLiteral(5.0))],
                [Assign(Id("x"),Id("y"))]))]))])
        expect = str(TypeMismatchInStatement(Assign(Id("x"),Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_44(self):
        """Test type mismatch assign statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"),[],StringLiteral("Dan"))],
                [Assign(Id("a"),BinaryOp("-",BinaryOp("*",BinaryOp("+",IntLiteral(2),IntLiteral(3)),
                BinaryOp("-",IntLiteral(4),IntLiteral(2))),BinaryOp("%",IntLiteral(5),IntLiteral(2))))]))])
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BinaryOp("-",BinaryOp("*",BinaryOp("+",IntLiteral(2),IntLiteral(3)),
                BinaryOp("-",IntLiteral(4),IntLiteral(2))),BinaryOp("%",IntLiteral(5),IntLiteral(2))))))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_45(self):
        """Test type mismatch in Do-While statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [Dowhile(([VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]),Id("x"))]))])
        expect = str(TypeMismatchInStatement(Dowhile(([VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]),Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_46(self):
        """Test type mismatch in Do-While statement"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [Dowhile(([VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]),StringLiteral("Dan"))]))])
        expect = str(TypeMismatchInStatement(Dowhile(([VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y")))]),StringLiteral("Dan"))))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_47(self):
        """Test type mismatch in func call statement"""
        input = Program([FuncDecl(Id("add_one"),[VarDecl(Id("n"),[],None)],([],[Return(BinaryOp("+",Id("n"),IntLiteral(1)))])),
                              FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],[CallStmt(Id("add_one"),[Id("x")])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("add_one"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_48(self):
        """Test type mismatch in func call statement"""
        input = """
                Var: x;
                Function: fact
                    Parameter: n
                    Body:
                        If n==0 Then
                            Return 1;
                        Else
                            Return n*fact(n-1);
                        EndIf.
                    EndBody.
                Function: main
                    Body:
                        x = 10;
                        fact(x);
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(CallStmt(Id("fact"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_49(self):
        """Test type mismatch in func call statement (invalid number of args)"""
        input = Program([FuncDecl(Id("main"),[],([],
                [CallStmt(Id("printStr"), [StringLiteral("Hi"), StringLiteral("Dan")])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStr"), [StringLiteral("Hi"), StringLiteral("Dan")])))
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_50(self):
        """Test type mismatch in func call statement (invalid type of args)"""
        input = Program([FuncDecl(Id("main"),[],([],
                [CallStmt(Id("printStr"), [IntLiteral(6)])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStr"), [IntLiteral(6)])))
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_51(self):
        """Test type mismatch in expression (array cell)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("arr"),[3],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]))
                ,VarDecl(Id("a"),[],IntLiteral(1)),VarDecl(Id("b"),[],IntLiteral(2)),VarDecl(Id("c"),[],None)],
                [Assign(Id("c"),BinaryOp("+",ArrayCell(Id("a"),[IntLiteral(3)]),Id("b")))]))])
        expect = str(TypeMismatchInExpression(ArrayCell(Id("a"),[IntLiteral(3)])))
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_52(self):
        """Test type mismatch in expression (array cell)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("arr"),[3],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]))
                ,VarDecl(Id("a"),[],FloatLiteral(1.0)),VarDecl(Id("b"),[],IntLiteral(2)),VarDecl(Id("c"),[],None)],
                [Assign(Id("c"),BinaryOp("+",ArrayCell(Id("arr"),[Id("a")]),Id("b")))]))])
        expect = str(TypeMismatchInExpression(ArrayCell(Id("arr"),[Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_53(self):
        """Test type mismatch in expression (array cell)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("arr"),[3],ArrayLiteral([FloatLiteral(1.0),FloatLiteral(2.0),FloatLiteral(3.0)]))
                ,VarDecl(Id("a"),[],IntLiteral(1)),VarDecl(Id("b"),[],IntLiteral(2)),VarDecl(Id("c"),[],None)],
                [Assign(Id("c"),BinaryOp("+",ArrayCell(Id("arr"),[IntLiteral(3)]),Id("b")))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("+",ArrayCell(Id("arr"),[IntLiteral(3)]),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_54(self):
        """Test type mismatch in expression (+ binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(4)),VarDecl(Id("y"),[],None)],
                [Assign(Id("y"),BinaryOp("+",Id("x"),FloatLiteral(6.0)))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("x"),FloatLiteral(6.0))))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_55(self):
        """Test type mismatch in expression (- binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(4)),VarDecl(Id("y"),[],IntLiteral(5)),
                VarDecl(Id("z"),[],FloatLiteral(6.0)), VarDecl(Id("t"),[],None)],
                [Assign(Id("t"),BinaryOp("-",BinaryOp("+",Id("x"),Id("y")),Id("z")))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("-",BinaryOp("+",Id("x"),Id("y")),Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_56(self):
        """Test type mismatch in expression (* binary operation)"""
        input = Program(
            [FuncDecl(Id("main"), [], ([VarDecl(Id("x"), [], IntLiteral(4)), VarDecl(Id("y"), [], FloatLiteral(5.0)),
            VarDecl(Id("z"), [], IntLiteral(6)), VarDecl(Id("t"), [], None)],
            [Assign(Id("t"),BinaryOp("-",BinaryOp("*",UnaryOp("-",Id("x")),Id("y")),BinaryOp("\\",Id("z"),UnaryOp("-",IntLiteral(5)))))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("*",UnaryOp("-",Id("x")),Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_57(self):
        """Test type mismatch in expression (\ binary operation)"""
        input = Program([FuncDecl(Id("main"), [], ([VarDecl(Id("x"), [], IntLiteral(4)), VarDecl(Id("y"), [], IntLiteral(5)),
                VarDecl(Id("z"), [], IntLiteral(6)), VarDecl(Id("t"), [], None)],
                [Assign(Id("t"),BinaryOp("-",BinaryOp("*",UnaryOp("-",Id("x")),Id("y")),BinaryOp("\\",Id("z"),UnaryOp("-.",FloatLiteral(5.0)))))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("\\",Id("z"),UnaryOp("-.",FloatLiteral(5.0)))))
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_58(self):
        """Test type mismatch in expression (% binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"), [], None)],
                [Assign(Id("a"),BinaryOp("-",BinaryOp("*",BinaryOp("+",IntLiteral(2),IntLiteral(3)),
                BinaryOp("-",IntLiteral(4),IntLiteral(2))),BinaryOp("%",IntLiteral(5),FloatLiteral(2.0))))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("%",IntLiteral(5),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_59(self):
        """Test type mismatch in expression (% binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(1),
                ([],
                [If([(BinaryOp("==",BinaryOp("%",Id("i"),FloatLiteral(2.0)),IntLiteral(0)),[],[Continue()])],([],[])),CallStmt(Id("print"),[Id("i")])]))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("%",Id("i"),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_60(self):
        """Test type mismatch in expression (- unary operation)"""
        input = Program([FuncDecl(Id("main"), [], ([VarDecl(Id("x"), [], FloatLiteral(4.0)), VarDecl(Id("y"), [], IntLiteral(5)),
                VarDecl(Id("z"), [], IntLiteral(6)), VarDecl(Id("t"), [], None)],
                [Assign(Id("t"),BinaryOp("-",BinaryOp("*",UnaryOp("-",Id("x")),Id("y")),BinaryOp("\\",Id("z"),UnaryOp("-",IntLiteral(5)))))]))])
        expect = str(TypeMismatchInExpression(UnaryOp("-",Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_61(self):
        """Test type mismatch in expression (- unary operation)"""
        input = Program([FuncDecl(Id("main"), [], ([VarDecl(Id("a"), [], None)],
                [Assign(Id("a"),BinaryOp("-",BinaryOp("*",BinaryOp("+",IntLiteral(2),UnaryOp("-",FloatLiteral(3))),
                BinaryOp("-",IntLiteral(4),UnaryOp("-",IntLiteral(2)))),BinaryOp("*",BinaryOp("%",IntLiteral(5),IntLiteral(2)),ArrayCell(Id("arr"),[BinaryOp("+",IntLiteral(0),Id("x"))]))))]))])
        expect = str(TypeMismatchInExpression(UnaryOp("-",FloatLiteral(3))))
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_62(self):
        """Test type mismatch in expression (- unary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("arr"),[3],ArrayLiteral([FloatLiteral(1.0),FloatLiteral(2.0),FloatLiteral(3.0)]))
                ,VarDecl(Id("a"),[],IntLiteral(1)),VarDecl(Id("b"),[],FloatLiteral(2.0)),VarDecl(Id("c"),[],None)],
                [Assign(Id("c"),BinaryOp("+.",UnaryOp("-", ArrayCell(Id("arr"),[IntLiteral(3)])),Id("b")))]))])
        expect = str(TypeMismatchInExpression(UnaryOp("-", ArrayCell(Id("arr"),[IntLiteral(3)]))))
        self.assertTrue(TestChecker.test(input,expect,462))

    def test_63(self):
        """Test type mismatch in expression (-. unary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("arr"),[3],ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]))
                ,VarDecl(Id("a"),[],IntLiteral(1)),VarDecl(Id("b"),[],FloatLiteral(2.0)),VarDecl(Id("c"),[],None)],
                [Assign(Id("c"),BinaryOp("+",UnaryOp("-.", ArrayCell(Id("arr"),[IntLiteral(3)])),Id("b")))]))])
        expect = str(TypeMismatchInExpression(UnaryOp("-.", ArrayCell(Id("arr"),[IntLiteral(3)]))))
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_64(self):
        """Test type mismatch in expression (- unary operation)"""
        input = Program([FuncDecl(Id("main"), [], ([VarDecl(Id("x"), [], IntLiteral(4)), VarDecl(Id("y"), [], IntLiteral(5)),
                VarDecl(Id("z"), [], IntLiteral(6)), VarDecl(Id("t"), [], None)],
                [Assign(Id("t"),BinaryOp("-",BinaryOp("*",UnaryOp("-.",Id("x")),Id("y")),BinaryOp("\\",Id("z"),UnaryOp("-",IntLiteral(5)))))]))])
        expect = str(TypeMismatchInExpression(UnaryOp("-.",Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_65(self):
        """Test type mismatch in expression (+. binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(45)),VarDecl(Id("y"),[],IntLiteral(52)),
                VarDecl(Id("z"),[],FloatLiteral(6.9)), VarDecl(Id("t"),[],None)],
                [Assign(Id("t"),BinaryOp("+.",BinaryOp("*",Id("x"),Id("y")),BinaryOp("*.",Id("z"),FloatLiteral(5e-10))))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("+.",BinaryOp("*",Id("x"),Id("y")),BinaryOp("*.",Id("z"),FloatLiteral(5e-10)))))
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_66(self):
        """Test type mismatch in expression (-. binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],FloatLiteral(4.5)),VarDecl(Id("y"),[],FloatLiteral(5.2e-1)),
                VarDecl(Id("z"),[],FloatLiteral(6.9)), VarDecl(Id("t"),[],None)],
                [Assign(Id("t"),BinaryOp("-.",BinaryOp("+.",BinaryOp("-.",Id("x"),Id("y")),Id("z")),IntLiteral(5)))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("-.",BinaryOp("+.",BinaryOp("-.",Id("x"),Id("y")),Id("z")),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_67(self):
        """Test type mismatch in expression (*. binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],FloatLiteral(4.5)),VarDecl(Id("y"),[],FloatLiteral(5.2e-1)),
                VarDecl(Id("z"),[],FloatLiteral(6.9)), VarDecl(Id("t"),[],None)],
                [Assign(Id("t"),BinaryOp("+.",BinaryOp("*.",Id("x"),Id("y")),BinaryOp("*.",Id("z"),FloatLiteral(5e-10)))),
                 Assign(Id("z"),BinaryOp("*.",Id("t"),IntLiteral(5)))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("*.",Id("t"),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_68(self):
        """Test type mismatch in expression (\. binary operation)"""
        input = Program([FuncDecl(Id("main"), [], (
                [VarDecl(Id("x"), [], IntLiteral(5)), VarDecl(Id("y"), [], FloatLiteral(5.2e-1)),
                VarDecl(Id("z"), [], FloatLiteral(6.9)), VarDecl(Id("t"), [], None)],
                [Assign(Id("t"),BinaryOp("\.", BinaryOp("*.", BinaryOp("\.", Id("x"), Id("y")), Id("z")), IntLiteral(5)))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("\.", Id("x"), Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_69(self):
        """Test type mismatch in expression (== binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [If([(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),FloatLiteral(1.0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),
                (BinaryOp(">",Id("x"),IntLiteral(0)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(2)))]),
                (BinaryOp(">",Id("x"),IntLiteral(100)),[],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(3)))])],
                ([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(4)))]))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("==",BinaryOp("%",Id("x"),IntLiteral(2)),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,469))

    def test_70(self):
        """Test type mismatch in expression (== binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [While(BinaryOp("<",Id("x"),FloatLiteral(10.5)),([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("<",Id("x"),FloatLiteral(10.5))))
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_71(self):
        """Test type mismatch in expression (=/= binary operation)"""
        input = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],IntLiteral(5))],
                [For(Id("i"),IntLiteral(0),BinaryOp("=/=",Id("i"),FloatLiteral(10.0)),BinaryOp("*",IntLiteral(1),IntLiteral(2)),
                ([VarDecl(Id("y"),[],IntLiteral(2))],
                [Assign(Id("x"),BinaryOp("+",Id("y"),Id("i")))]))]))])
        expect = str(TypeMismatchInExpression(BinaryOp("=/=",Id("i"),FloatLiteral(10.0))))
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_72(self):
        """Test type mismatch in expression (>=. binary operation)"""
        input = """
                Function: main
                    Body:
                        Var: x = 0.5, y, z;
                        y = 12 * 5;
                        z = x <=. y;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("<=.",Id("x"), Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_73(self):
        """Test type mismatch in expression (! unary operation)"""
        input = """
                Function: main
                    Body:
                        Var: a = 1, b = False, c;
                        c = !a && b;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("!",Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_74(self):
        """Test type mismatch in expression (&& binary operation)"""
        input = """
                Function: main
                    Body:
                        Var: a = True, b = 4, c;
                        c = a && b;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("&&",Id("a"),Id("b"))))
        self.assertTrue(TestChecker.test(input,expect,474))

    def test_75(self):
        """Test type mismatch in expression (&& binary operation)"""
        input = """
                Function: main
                    Body:
                        Var: a = True, b = False, c;
                        c = a && b || 3;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("||",BinaryOp("&&",Id("a"),Id("b")),IntLiteral(3))))
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_76(self):
        """Test type mismatch in call expression (wrong param number)"""
        input = """
                Function: add
                    Parameter: a, b
                    Body:
                        Return a + b;
                    EndBody.
                Function: main
                    Body:
                        Var: x = 5, y = 10;
                        print(add(x));
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id("add"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_77(self):
        """Test type mismatch in call expression (wrong param type)"""
        input = """
                Function: add_one
                    Parameter: n
                    Body:
                        Return n + 1;
                    EndBody.
                Function: main
                    Body:
                        Var: x = 5.0;
                        x = add_one(x) + 1;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id("add_one"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_78(self):
        """Test type mismatch in call expression (wrong param type)"""
        input = """
                Var: x;
                Function: fact
                    Parameter: n
                    Body:
                        If n==0 Then
                            Return 1;
                        Else
                            Return n*fact(n-1);
                        EndIf.
                    EndBody.
                Function: main
                    Body:
                        x = fact(5.0);
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id("fact"),[FloatLiteral(5.0)])))
        self.assertTrue(TestChecker.test(input,expect,478))

    def test_79(self):
        """Test type mismatch in call expression (wrong param type)"""
        input = """
                Var: x = 1.0;
                Function: fact
                    Parameter: n
                    Body:
                        If n==0 Then
                            Return 1;
                        Else
                            Return n*fact(n-1);
                        EndIf.
                    EndBody.
                Function: main
                    Body:
                        x = fact(5);
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("fact"), [IntLiteral(5)]))))
        self.assertTrue(TestChecker.test(input,expect,479))

    def test_80(self):
        """Test type mismatch in call expression (wrong param type)"""
        input = """
                Function: add_one
                    Parameter: n
                    Body:
                        Return n + 1;
                    EndBody.
                Function: main
                    Body:
                        Var: x = 5;
                        x = add_one(x) + 1.0;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("+", CallExpr(Id("add_one"),[Id("x")]), FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,480))

    def test_81(self):
        """Test type cannot be inferred (assign statement - Id)"""
        input = """
                Function: main
                    Body:
                        Var: x, y;
                        x = y;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id("x"), Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_82(self):
        """Test type cannot be inferred (assign statement - array cell)"""
        input = """
                Function: main
                    Body:
                        Var: arr[3], y;
                        arr[1] = y;
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(Id("arr"), [IntLiteral(1)]), Id("y"))))
        self.assertTrue(TestChecker.test(input,expect,482))

    def test_83(self):
        """Test type cannot be inferred (function call)"""
        input = """
                Function: add
                    Parameter: a, b
                    Body:
                        printStr("hello");
                    EndBody.
                Function: main
                    Body:
                        Var: x = 5, y;
                        add(x, y);
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(CallStmt(Id("add"),[Id("x"),Id("y")])))
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_84(self):
        """Test type cannot be inferred (function call)"""
        input = """
                Function: hello
                    Parameter: name
                    Body:
                        printStr(name);
                    EndBody.
                Function: main
                    Body:
                        Var: n;
                        hello(n);
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(CallStmt(Id("hello"),[Id("n")])))
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_85(self):
        """Test type cannot be inferred (if statement)"""
        input = """
                Function: main
                    Body:
                        Var: x;
                        If x Then
                            printStr("if statement");
                        Else
                            printStr("else statement");
                        EndIf.
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(If([(Id("x"),[],[CallStmt(Id("printStr"),[StringLiteral("if statement")])])],
                ([],[CallStmt(Id("printStr"),[StringLiteral("else statement")])]))))
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test_86(self):
        """Test type cannot be inferred (if statement)"""
        input = """
                Function: main
                    Body:
                        Var: x;
                        If False Then
                            printStr("if statement");
                        ElseIf x Then
                            printStr("else if statement");
                        Else
                            printStr("else statement");
                        EndIf.
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(If([(BooleanLiteral(False),[],[CallStmt(Id("printStr"),[StringLiteral("if statement")])]),
                                              (Id("x"),[],[CallStmt(Id("printStr"),[StringLiteral("else if statement")])])],
                ([],[CallStmt(Id("printStr"),[StringLiteral("else statement")])]))))
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_87(self):
        """Test type cannot be inferred (for statement)"""
        input = """
                Function: main
                    Body:
                        Var: x;
                        For (i = x, i < 10, 1) Do
                            If i > 5 Then
                                Break;
                            EndIf.
                            print(i);
                        EndFor.
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(For(Id("i"),Id("x"),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(1),
                ([],
                [If([(BinaryOp(">",Id("i"),IntLiteral(5)),[],[Break()])],([],[])),CallStmt(Id("print"),[Id("i")])]))))
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_88(self):
        """Test type cannot be inferred (for statement)"""
        input = """
                Function: main
                    Body:
                        Var: x;
                        For (i = 0, i < 10, x) Do
                            If i > 5 Then
                                Break;
                            EndIf.
                            print(i);
                        EndFor.
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),Id("x"),
                ([],
                [If([(BinaryOp(">",Id("i"),IntLiteral(5)),[],[Break()])],([],[])),CallStmt(Id("print"),[Id("i")])]))))
        self.assertTrue(TestChecker.test(input, expect, 488))

    def test_89(self):
        """Test type cannot be inferred (return statement)"""
        input = """
                Function: foo
                    Parameter: n
                    Body:
                        Var: x;
                        Return x;
                    EndBody.
                Function: main
                    Body:
                        Var: x = 5;
                        foo(x);
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Return(Id("x"))))
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test_90(self):
        """Test type cannot be inferred (Do-while statement)"""
        input = """
                Function: main
                    Body:
                        Var: x = 5, y;
                        Do
                            x = x + 1;
                        While y
                        EndDo.
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Dowhile(([],[Assign(Id("x"),BinaryOp("+",Id("x"),IntLiteral(1)))]),Id("y"))))
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test_91(self):
        """Test type cannot be inferred (while statement)"""
        input = """
                Function: main
                    Body:
                        Var: x = 5, y;
                        While y Do
                            Var: y = 5;
                            x = x + y;
                            If x >= 50 Then
                                Break;
                            EndIf.
                        EndWhile.
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(While(Id("y"),(
                [VarDecl(Id("y"),[],IntLiteral(5))],
                [Assign(Id("x"),BinaryOp("+",Id("x"),Id("y"))),
                 If([(BinaryOp(">=",Id("x"),IntLiteral(50)),[],[Break()])],([],[]))]))))
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test_92(self):
        """Test type cannot be inferred (while statement)"""
        input = """
                Function: foo
                    Parameter: n
                    Body:
                        Return 1;
                    EndBody.
                Function: main
                    Body:
                        Var: x, y, a = 1;
                        y = a + foo(x);
                    EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id("y"), BinaryOp("+", Id("a"), CallExpr(Id("foo"),[Id("x")])))))
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_93(self):
        """Test type inferre"""
        input = """
                Function: add_one
                    Parameter: n
                    Body:
                        Return n + 1;
                    EndBody.
                Function: main
                    Body:
                        Var: x = 5, y, z;
                        y = add_one(x);
                        z = y;
                        z = -.z;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-.", Id("z"))))
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_94(self):
        """Test type inferre"""
        input = """
                Function: add_one
                    Parameter: n
                    Body:
                        Return n + 1;
                    EndBody.
                Function: main
                    Body:
                        Var: arr[3], x = 5, y = 2.0;
                        arr[0] = x;
                        arr[1] = add_one(x);
                        arr[2] = y;
                    EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("arr"),[IntLiteral(2)]), Id("y"))))
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_95(self):
        """Test type inferre"""
        input = """
                Var: x;
                Function: fact
                    Parameter: n
                    Body:
                        If n==0 Then
                            Return 1;
                        Else
                            Return n*fact(n-1);
                        EndIf.
                    EndBody.
                Function: main
                    Body:
                        x = fact(10);
                        x = !x;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("!", Id("x"))))
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test_96(self):
        """Test type inferre"""
        input = """
                Function: main
                    Body:
                        Var: x, y, z, t;
                        x = y + z;
                        t = x *. z;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("*.", Id("x"), Id("z"))))
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test_97(self):
        """Test type inferre"""
        input = """
                Function: main
                    Body:
                        Var: x, y, z, t;
                        x = y -. z;
                        t = ---y;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-", Id("y"))))
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_98(self):
        """Test type inferre"""
        input = """
            Function: main
                Body:
                    Var: arr[3], x = 5, y = 2.0;
                    arr[y] = x;
                EndBody.
            """
        expect = str(TypeMismatchInExpression(ArrayCell(Id("arr"), [Id("y")])))
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test_99(self):
        """Test type inferre"""
        input = """
                Function: foo
                    Body:
                        Var: res[3] = {1, 2, 3};
                        Return res;
                    EndBody.
                Function: main
                    Body:
                        Var: x, y;
                        x = foo();
                        y = x[0] *. 2.5;
                    EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("*.", ArrayCell(Id("x"), [IntLiteral(0)]), FloatLiteral(2.5))))
        self.assertTrue(TestChecker.test(input, expect, 499))

    def test_100(self):
        """Test type inferre"""
        input = """
                Function: foo
                    Body:
                        Var: res[3] = {1, 2, 3};
                        Return res;
                    EndBody.
                Function: foo1
                    Body:
                        Var: x, y;
                        x = foo();
                        y = x[0] * 2;
                    EndBody.
                """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input, expect, 500))
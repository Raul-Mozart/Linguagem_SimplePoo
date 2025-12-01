@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00"

; ModuleID = 'SimplePOO'
target triple = "x86_64-pc-linux-gnu"

declare i32 @printf(i8*, ...)

define void @main() {
  entry:
    %0 = alloca i64
    store i64 0, i64* %0
    br label %for.cond0
  for.cond0:
    %1 = load i64, i64* %0
    %2 = icmp slt i64 %1, 5
    br i1 %2, label %for.body1, label %for.end3
  for.body1:
    %3 = load i64, i64* %0
    %4 = getelementptr [4 x i8], [4 x i8]* @.str, i32 0, i32 0
    call i32 (i8*, ...) @printf(i8* %4, i64 %3)
    br label %for.update2
  for.update2:
    br label %for.cond0
  for.end3:
    ret void
}

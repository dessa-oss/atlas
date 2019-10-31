##################################################################
#                                                               ##
#   WildFly Elytron Tool Script for Windows                     ##
#                                                               ##
##################################################################
$scripts = (Get-ChildItem $MyInvocation.MyCommand.Path).Directory.FullName;
. $scripts'\common.ps1'

$SCRIPT_NAME = $MyInvocation.MyCommand | select -ExpandProperty Name
$SCRIPT_NAME = "{" + $SCRIPT_NAME + "}"

$ELYTRON_TOOL_OPTS=@()
if ($ARGS.Count -gt 0){
  $ELYTRON_TOOL_OPTS+=$SCRIPT_NAME + $ARGS[0]
  $ELYTRON_TOOL_OPTS+=$ARGS[1..$ARGS.Count]
}

$JAVA_OPTS = @()

if ($env:ELYTRON_TOOL_ADDONS) {
    $ELYTRON_TOOL_SEP = ";"
}

# Sample JPDA settings for remote socket debugging
#$JAVA_OPTS+="-agentlib:jdwp=transport=dt_socket,address=8787,server=y,suspend=y"

& $JAVA $JAVA_OPTS -cp $JBOSS_HOME'\bin\wildfly-elytron-tool.jar'$ELYTRON_TOOL_SEP$env:ELYTRON_TOOL_ADDONS org.wildfly.security.tool.ElytronTool $ELYTRON_TOOL_OPTS

Env-Clean-Up

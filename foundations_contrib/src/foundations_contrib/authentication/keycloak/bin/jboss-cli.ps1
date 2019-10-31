#############################################################################
#                                                                          ##
#    WildFly CLI Script for interacting with the server                    ##
#                                                                          ##
#############################################################################
$PROGNAME=$MyInvocation.MyCommand.Name
$scripts = (Get-ChildItem $MyInvocation.MyCommand.Path).Directory.FullName;
. $scripts'\common.ps1'

$SERVER_OPTS = Process-Script-Parameters -Params $ARGS

# Override ibm JRE behavior
$IBM_TLS_OPT = "-Dcom.ibm.jsse2.overrideDefaultTLS=true"

$PROG_ARGS = Get-Java-Arguments -entryModule "org.jboss.as.cli" -serverOpts $SERVER_OPTS -logFileProperties "$JBOSS_HOME/bin/jboss-cli-logging.properties"

& $JAVA $IBM_TLS_OPT $PROG_ARGS

Env-Clean-Up

exit $LASTEXITCODE
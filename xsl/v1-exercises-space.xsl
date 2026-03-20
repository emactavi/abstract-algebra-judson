<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:import href="./v2-exercises.xsl"/>

<!-- Append spacing after every divisionsolution environment -->
<xsl:param name="latex.preamble.late">
    <xsl:text>\tcbset{ divisionsolutionstyle/.append style={after={\vspace*{8\baselineskip}}} }&#xa;</xsl:text>
</xsl:param>

</xsl:stylesheet>

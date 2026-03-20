<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
    xmlns:exsl="http://exslt.org/common"
    extension-element-prefixes="exsl"
>

<!-- Import the solution manual stylesheet -->
<xsl:import href="./core/pretext-solution-manual-latex.xsl"/>

<!-- Show exercise statements -->
<xsl:param name="exercise.divisional.statement" select="'yes'"/>
<xsl:param name="exercise.divisional.hint"      select="'no'"/>
<xsl:param name="exercise.divisional.answer"    select="'no'"/>
<xsl:param name="exercise.divisional.solution"  select="'no'"/>

<!-- Show reading question statements -->
<xsl:param name="exercise.reading.statement"    select="'yes'"/>
<xsl:param name="exercise.reading.hint"         select="'no'"/>
<xsl:param name="exercise.reading.answer"       select="'no'"/>
<xsl:param name="exercise.reading.solution"     select="'no'"/>

<!-- Hide inline exercises and other types -->
<xsl:param name="exercise.inline.statement"     select="'no'"/>
<xsl:param name="exercise.worksheet.statement"  select="'no'"/>
<xsl:param name="project.statement"             select="'no'"/>

</xsl:stylesheet>

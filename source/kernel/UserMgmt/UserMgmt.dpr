library UserMgmt;

{ Important note about DLL memory management: ShareMem must be the
  first unit in your library's USES clause AND your project's (select
  Project-View Source) USES clause if your DLL exports any procedures or
  functions that pass strings as parameters or function results. This
  applies to all strings passed to and from your DLL--even those that
  are nested in records and classes. ShareMem is the interface unit to
  the BORLNDMM.DLL shared memory manager, which must be deployed along
  with your DLL. To avoid using BORLNDMM.DLL, pass string information
  using PChar or ShortString parameters. }

(*
  Business object module project file
  This program is generated by EASY DAF 2.0i
*)

uses
  ShareMem,
  PClassIntf in '..\..\PClassIntf.pas',
  PModClsDecl in 'PModClsDecl.pas',
  PModExport in 'PModExport.pas',
  ModUserMgmt in 'ModUserMgmt.pas',
  SysUtils,
  Classes;

{$R *.RES}

begin
  {Put any necessary initialization here}
end.